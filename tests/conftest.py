import os
os.environ["TESTING"] = "True"

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool
from unittest.mock import patch, AsyncMock
from fastapi import FastAPI
from fastapi_mail import ConnectionConfig

from src.database.models import Base, User
from src.database.session import get_async_db
from src.main import app
from src.repository.users import create_user
from src.schemas import UserCreate
from src.services.auth import auth_service
from src.services.limiter import limiter

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=True
)
TestingSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

@pytest.fixture(scope="function", autouse=True)
def reset_limiter():
    # Reset the rate limiter before each test
    limiter.reset()
    yield

@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    # Create tables at the start of each test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Clean up after each test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def db():
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()

async def override_get_db():
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()

# Override the database dependency
app.dependency_overrides[get_async_db] = override_get_db

@pytest.fixture(scope="function")
def test_user():
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "confirm_password": "testpassword123",
        "full_name": "Test User"
    }

@pytest.fixture(scope="function")
async def mock_email_service():
    with patch('src.services.email.send_verification_email', AsyncMock(return_value=True)), \
         patch('src.services.email.send_email', AsyncMock(return_value=True)), \
         patch('src.services.email.send_password_reset_email', AsyncMock(return_value=True)):
        yield

@pytest_asyncio.fixture
async def async_client(mock_email_service):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        follow_redirects=True
    ) as ac:
        yield ac

@pytest_asyncio.fixture
async def authenticated_client(async_client, test_user, db):
    # Create test user in DB
    user_data = test_user.copy()
    user_data["email"] = "auth_test@example.com"  # Use a different email to avoid conflicts
    hashed_password = auth_service.get_password_hash(user_data["password"])
    db_user = await create_user(
        db,
        email=user_data["email"],
        hashed_password=hashed_password,
        full_name=user_data["full_name"]
    )
    await db.commit()
    
    # Verify email
    token = await auth_service.create_verification_token({"sub": user_data["email"]})
    await async_client.post(f"/api/auth/verify/{token}")
    
    # Login to get token
    response = await async_client.post("/api/auth/login", 
                               data={
                                   "username": user_data["email"],
                                   "password": user_data["password"]
                               })
    token = response.json()["access_token"]
    
    # Create new client with auth headers
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        headers={"Authorization": f"Bearer {token}"},
        follow_redirects=True
    ) as ac:
        yield ac

@pytest.fixture
def test_contact():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "birthday": "1990-01-01",
        "notes": "Test contact"
    }