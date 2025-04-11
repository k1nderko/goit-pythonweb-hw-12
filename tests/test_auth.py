import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient
from tests.utils import patch_email_service
from src.schemas import UserCreate
from src.services.auth import auth_service
from src.repository.users import get_user_by_email, create_user
from src.main import app

@pytest.mark.asyncio
async def test_register_user(async_client, test_user, db):
    response = await async_client.post("/api/auth/register", json=test_user)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == test_user["email"]
    assert "id" in data

@pytest.mark.asyncio
async def test_register_user_duplicate_email(async_client, test_user, db):
    # First registration
    await async_client.post("/api/auth/register", json=test_user)
    # Second registration with same email
    response = await async_client.post("/api/auth/register", json=test_user)
    assert response.status_code == status.HTTP_409_CONFLICT

@pytest.mark.asyncio
async def test_login_user(async_client: AsyncClient):
    with patch_email_service():
        # Register a user first
        response = await async_client.post(
            "/api/auth/register",
            json={
                "email": "login@example.com",
                "password": "testpassword123",
                "confirm_password": "testpassword123",
                "full_name": "Test User"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED

        # Verify email
        verification_token = await auth_service.create_verification_token({"sub": "login@example.com"})
        response = await async_client.post(f"/api/auth/verify/{verification_token}")
        assert response.status_code == status.HTTP_200_OK

        # Login
        response = await async_client.post(
            "/api/auth/login",
            data={
                "username": "login@example.com",
                "password": "testpassword123"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert "token_type" in response.json()
        assert response.json()["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_user_invalid_credentials(async_client, test_user, db):
    # Create user first
    hashed_password = auth_service.get_password_hash(test_user["password"])
    user = await create_user(
        db,
        email=test_user["email"],
        hashed_password=hashed_password,
        full_name=test_user["full_name"]
    )
    user.is_verified = True
    await db.commit()
    
    login_data = {
        "username": test_user["email"],
        "password": "wrongpassword"
    }
    response = await async_client.post("/api/auth/login", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_get_current_user(async_client: AsyncClient):
    with patch_email_service():
        # Register a user first
        response = await async_client.post(
            "/api/auth/register",
            json={
                "email": "current@example.com",
                "password": "testpassword123",
                "confirm_password": "testpassword123",
                "full_name": "Test User"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED

        # Verify email
        verification_token = await auth_service.create_verification_token({"sub": "current@example.com"})
        response = await async_client.post(f"/api/auth/verify/{verification_token}")
        assert response.status_code == status.HTTP_200_OK

        # Login
        response = await async_client.post(
            "/api/auth/login",
            data={
                "username": "current@example.com",
                "password": "testpassword123"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        access_token = response.json()["access_token"]

        # Get current user
        response = await async_client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["email"] == "current@example.com"

@pytest.mark.asyncio
async def test_get_current_user_invalid_token(async_client):
    headers = {"Authorization": "Bearer invalid_token"}
    response = await async_client.get("/api/auth/me", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_verify_email(async_client: AsyncClient):
    with patch_email_service():
        # Register a user first
        response = await async_client.post(
            "/api/auth/register",
            json={
                "email": "verify@example.com",
                "password": "testpassword123",
                "confirm_password": "testpassword123",
                "full_name": "Test User"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED

        # Create verification token
        verification_token = await auth_service.create_verification_token({"sub": "verify@example.com"})

        # Verify email
        response = await async_client.post(f"/api/auth/verify/{verification_token}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "Email verified successfully"

@pytest.mark.asyncio
async def test_verify_email_invalid_token(async_client: AsyncClient):
    with patch_email_service():
        # Register a user first
        response = await async_client.post(
            "/api/auth/register",
            json={
                "email": "verify_invalid@example.com",
                "password": "testpassword123",
                "confirm_password": "testpassword123",
                "full_name": "Test User"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED

        # Try to verify with invalid token
        response = await async_client.post("/api/auth/verify/invalid_token")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json()["detail"] == "Invalid or expired verification token" 