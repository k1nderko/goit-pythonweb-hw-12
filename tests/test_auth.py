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
async def test_login_user(async_client, test_user, db):
    # Create and verify user
    user = await create_user(db, UserCreate(**test_user))
    user.is_verified = True
    await db.commit()
    
    # Login
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    response = await async_client.post("/api/auth/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_user_invalid_credentials(async_client, test_user, db):
    # Create user first
    user = await create_user(db, UserCreate(**test_user))
    user.is_verified = True
    await db.commit()
    
    login_data = {
        "username": test_user["email"],
        "password": "wrongpassword"
    }
    response = await async_client.post("/api/auth/login", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_get_current_user(async_client, test_user, db):
    # Create and verify user
    user = await create_user(db, UserCreate(**test_user))
    user.is_verified = True
    await db.commit()
    
    # Login to get token
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    login_response = await async_client.post("/api/auth/login", data=login_data)
    token = login_response.json()["access_token"]
    
    # Get current user
    headers = {"Authorization": f"Bearer {token}"}
    response = await async_client.get("/api/auth/me", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_user["email"]

@pytest.mark.asyncio
async def test_get_current_user_invalid_token(async_client):
    headers = {"Authorization": "Bearer invalid_token"}
    response = await async_client.get("/api/auth/me", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_verify_email(async_client, test_user, db):
    """Test email verification process."""
    # Create an unverified user
    user = await create_user(db, UserCreate(**test_user))
    assert user is not None
    assert not user.is_verified

    # Create verification token
    token = auth_service.create_verification_token(test_user["email"])

    # Verify email
    response = await async_client.get(f"/api/auth/verify/{token}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Email verified successfully"

    # Refresh the session to ensure we have the latest state
    db.expire_all()
    
    # Check that user is now verified
    updated_user = await get_user_by_email(db, test_user["email"])
    assert updated_user.is_verified

@pytest.mark.asyncio
async def test_verify_email_invalid_token(async_client, db):
    response = await async_client.get("/api/auth/verify/invalid_token")
    assert response.status_code == status.HTTP_400_BAD_REQUEST 