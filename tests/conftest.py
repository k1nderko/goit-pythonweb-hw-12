import os
os.environ["TESTING"] = "True"

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool
from unittest.mock import patch, AsyncMock
from fastapi import FastAPI

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
)
TestingSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

@pytest.fixture(scope="function", autouse=True)
def reset_limiter():
    # Reset the rate limiter before each test
    limiter.reset()
    yield

@pytest_asyncio.fixture(scope="function")
async def db():
    # Create tables at the start of each test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
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
def mock_email_service(monkeypatch):
    async def mock_send_verification_email(to_email: str, token: str):
        return True
        
    monkeypatch.setattr("src.services.email.send_verification_email", mock_send_verification_email)
    return mock_send_verification_email

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
    db_user = await create_user(db, UserCreate(**user_data))
    await db.commit()
    
    # Verify email
    token = auth_service.create_verification_token(user_data["email"])
    await async_client.get(f"/api/auth/verify/{token}")
    
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

def patch_email_service():
    return patch("src.services.email.send_verification_email", AsyncMock(return_value=True))