import pytest
from fastapi import status
from httpx import AsyncClient
from tests.utils import patch_email_service
from src.services.limiter import limiter
from src.services.auth import auth_service

@pytest.mark.asyncio
async def test_rate_limit_root_endpoint(async_client: AsyncClient):
    # Reset the limiter before the test
    limiter.reset()
    
    # Make 5 requests to the root endpoint
    for _ in range(5):
        response = await async_client.get("/")
        assert response.status_code == status.HTTP_200_OK

    # The 6th request should be rate limited
    response = await async_client.get("/")
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS

@pytest.mark.asyncio
async def test_rate_limit_auth_endpoints(async_client: AsyncClient, db):
    # Reset the limiter before the test
    limiter.reset()

    with patch_email_service():
        # Register a user
        response = await async_client.post(
            "/api/auth/register",
            json={
                "email": "ratelimit@example.com",
                "password": "testpassword123",
                "confirm_password": "testpassword123",
                "full_name": "Test User"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED

        # Verify the user's email
        token = auth_service.create_verification_token("ratelimit@example.com")
        response = await async_client.get(f"/api/auth/verify/{token}")
        assert response.status_code == status.HTTP_200_OK

        # Make 5 login attempts
        for _ in range(5):
            response = await async_client.post(
                "/api/auth/login",
                data={
                    "username": "ratelimit@example.com",
                    "password": "testpassword123"
                }
            )
            assert response.status_code == status.HTTP_200_OK

        # The 6th attempt should be rate limited
        response = await async_client.post(
            "/api/auth/login",
            data={
                "username": "ratelimit@example.com",
                "password": "testpassword123"
            }
        )
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS

@pytest.mark.asyncio
async def test_rate_limit_reset(async_client: AsyncClient):
    # Reset the limiter before the test
    limiter.reset()
    
    # Make 5 requests to the root endpoint
    for _ in range(5):
        response = await async_client.get("/")
        assert response.status_code == status.HTTP_200_OK

    # The 6th request should be rate limited
    response = await async_client.get("/")
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS

    # Reset the limiter
    limiter.reset()

    # After reset, should be able to make requests again
    response = await async_client.get("/")
    assert response.status_code == status.HTTP_200_OK 