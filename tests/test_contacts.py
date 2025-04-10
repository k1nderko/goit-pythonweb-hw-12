import pytest
from fastapi import status
from httpx import AsyncClient
from tests.utils import patch_email_service
from src.services.auth import auth_service

@pytest.mark.asyncio
async def test_create_contact(async_client: AsyncClient):
    with patch_email_service():
        # Register and login first
        register_response = await async_client.post(
            "/api/auth/register",
            json={
                "email": "contact@example.com",
                "password": "testpassword123",
                "confirm_password": "testpassword123",
                "full_name": "Test User"
            }
        )
        assert register_response.status_code == status.HTTP_201_CREATED
        
        # Verify email
        verification_token = auth_service.create_verification_token("contact@example.com")
        await async_client.get(f"/api/auth/verify/{verification_token}")
        
        # Login
        login_response = await async_client.post(
            "/api/auth/login",
            data={
                "username": "contact@example.com",
                "password": "testpassword123"
            }
        )
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.json()["access_token"]
        
        # Create contact
        response = await async_client.post(
            "/api/contacts",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "phone": "+1234567890",
                "birthday": "1990-01-01",
                "notes": "Test contact"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "id" in data
        assert "owner_id" in data
        assert data["first_name"] == "John"
        assert data["last_name"] == "Doe"
        assert data["email"] == "john@example.com"
        assert data["phone"] == "+1234567890"
        assert data["birthday"] == "1990-01-01"
        assert data["notes"] == "Test contact"

@pytest.mark.asyncio
async def test_create_contact_unauthorized(async_client: AsyncClient):
    response = await async_client.post(
        "/api/contacts",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "birthday": "1990-01-01",
            "notes": "Test contact"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert "detail" in data
    assert "not authenticated" in data["detail"].lower()

@pytest.mark.asyncio
async def test_get_contacts(async_client: AsyncClient):
    with patch_email_service():
        # Register and login first
        register_response = await async_client.post(
            "/api/auth/register",
            json={
                "email": "contacts@example.com",
                "password": "testpassword123",
                "confirm_password": "testpassword123",
                "full_name": "Test User"
            }
        )
        assert register_response.status_code == status.HTTP_201_CREATED
        
        # Verify email
        verification_token = auth_service.create_verification_token("contacts@example.com")
        await async_client.get(f"/api/auth/verify/{verification_token}")
        
        # Login
        login_response = await async_client.post(
            "/api/auth/login",
            data={
                "username": "contacts@example.com",
                "password": "testpassword123"
            }
        )
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.json()["access_token"]
        
        # Get contacts
        response = await async_client.get(
            "/api/contacts",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

@pytest.mark.asyncio
async def test_get_contact_by_id(async_client: AsyncClient):
    with patch_email_service():
        # Register and login first
        register_response = await async_client.post(
            "/api/auth/register",
            json={
                "email": "getcontact@example.com",
                "password": "testpassword123",
                "confirm_password": "testpassword123",
                "full_name": "Test User"
            }
        )
        assert register_response.status_code == status.HTTP_201_CREATED
        
        # Verify email
        verification_token = auth_service.create_verification_token("getcontact@example.com")
        await async_client.get(f"/api/auth/verify/{verification_token}")
        
        # Login
        login_response = await async_client.post(
            "/api/auth/login",
            data={
                "username": "getcontact@example.com",
                "password": "testpassword123"
            }
        )
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.json()["access_token"]
        
        # Create a contact first
        create_response = await async_client.post(
            "/api/contacts",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "phone": "+1234567890",
                "birthday": "1990-01-01",
                "notes": "Test contact"
            }
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        contact_id = create_response.json()["id"]
        
        # Get contact by ID
        response = await async_client.get(
            f"/api/contacts/{contact_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == contact_id
        assert data["first_name"] == "John"
        assert data["last_name"] == "Doe"

@pytest.mark.asyncio
async def test_update_contact(async_client: AsyncClient):
    with patch_email_service():
        # Register and login first
        register_response = await async_client.post(
            "/api/auth/register",
            json={
                "email": "updatecontact@example.com",
                "password": "testpassword123",
                "confirm_password": "testpassword123",
                "full_name": "Test User"
            }
        )
        assert register_response.status_code == status.HTTP_201_CREATED
        
        # Verify email
        verification_token = auth_service.create_verification_token("updatecontact@example.com")
        await async_client.get(f"/api/auth/verify/{verification_token}")
        
        # Login
        login_response = await async_client.post(
            "/api/auth/login",
            data={
                "username": "updatecontact@example.com",
                "password": "testpassword123"
            }
        )
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.json()["access_token"]
        
        # Create a contact first
        create_response = await async_client.post(
            "/api/contacts",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "phone": "+1234567890",
                "birthday": "1990-01-01",
                "notes": "Test contact"
            }
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        contact_id = create_response.json()["id"]
        
        # Update contact
        response = await async_client.put(
            f"/api/contacts/{contact_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "jane@example.com",
                "phone": "+0987654321",
                "birthday": "1991-01-01",
                "notes": "Updated contact"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == contact_id
        assert data["first_name"] == "Jane"
        assert data["last_name"] == "Doe"
        assert data["email"] == "jane@example.com"

@pytest.mark.asyncio
async def test_delete_contact(async_client: AsyncClient):
    with patch_email_service():
        # Register and login first
        register_response = await async_client.post(
            "/api/auth/register",
            json={
                "email": "deletecontact@example.com",
                "password": "testpassword123",
                "confirm_password": "testpassword123",
                "full_name": "Test User"
            }
        )
        assert register_response.status_code == status.HTTP_201_CREATED
        
        # Verify email
        verification_token = auth_service.create_verification_token("deletecontact@example.com")
        await async_client.get(f"/api/auth/verify/{verification_token}")
        
        # Login
        login_response = await async_client.post(
            "/api/auth/login",
            data={
                "username": "deletecontact@example.com",
                "password": "testpassword123"
            }
        )
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.json()["access_token"]
        
        # Create a contact first
        create_response = await async_client.post(
            "/api/contacts",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "phone": "+1234567890",
                "birthday": "1990-01-01",
                "notes": "Test contact"
            }
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        contact_id = create_response.json()["id"]
        
        # Delete contact
        response = await async_client.delete(
            f"/api/contacts/{contact_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify contact is deleted
        get_response = await async_client.get(
            f"/api/contacts/{contact_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_search_contacts(async_client: AsyncClient):
    with patch_email_service():
        # Register and login first
        register_response = await async_client.post(
            "/api/auth/register",
            json={
                "email": "searchcontact@example.com",
                "password": "testpassword123",
                "confirm_password": "testpassword123",
                "full_name": "Test User"
            }
        )
        assert register_response.status_code == status.HTTP_201_CREATED
        
        # Verify email
        verification_token = auth_service.create_verification_token("searchcontact@example.com")
        await async_client.get(f"/api/auth/verify/{verification_token}")
        
        # Login
        login_response = await async_client.post(
            "/api/auth/login",
            data={
                "username": "searchcontact@example.com",
                "password": "testpassword123"
            }
        )
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.json()["access_token"]
        
        # Create contacts
        await async_client.post(
            "/api/contacts",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "phone": "+1234567890",
                "birthday": "1990-01-01",
                "notes": "Test contact"
            }
        )
        
        await async_client.post(
            "/api/contacts",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "jane@example.com",
                "phone": "+0987654321",
                "birthday": "1991-01-01",
                "notes": "Test contact"
            }
        )
        
        # Search contacts
        response = await async_client.get(
            "/api/contacts/search?query=Doe",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert all(contact["last_name"] == "Doe" for contact in data)

@pytest.mark.asyncio
async def test_search_contacts_by_email(async_client: AsyncClient):
    with patch_email_service():
        # Register and login first
        register_response = await async_client.post(
            "/api/auth/register",
            json={
                "email": "searchbyemail@example.com",
                "password": "testpassword123",
                "confirm_password": "testpassword123",
                "full_name": "Test User"
            }
        )
        assert register_response.status_code == status.HTTP_201_CREATED
        
        # Verify email
        verification_token = auth_service.create_verification_token("searchbyemail@example.com")
        await async_client.get(f"/api/auth/verify/{verification_token}")
        
        # Login
        login_response = await async_client.post(
            "/api/auth/login",
            data={
                "username": "searchbyemail@example.com",
                "password": "testpassword123"
            }
        )
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.json()["access_token"]
        
        # Create contacts
        await async_client.post(
            "/api/contacts",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "first_name": "John",
                "last_name": "Smith",
                "email": "john.smith@example.com",
                "phone": "+1234567890",
                "birthday": "1990-01-01",
                "notes": "Test contact"
            }
        )
        
        await async_client.post(
            "/api/contacts",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "jane.smith@example.com",
                "phone": "+0987654321",
                "birthday": "1991-01-01",
                "notes": "Test contact"
            }
        )
        
        # Search contacts by email
        response = await async_client.get(
            "/api/contacts/search?query=smith@example.com",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert all("smith@example.com" in contact["email"] for contact in data)

@pytest.mark.asyncio
async def test_search_contacts_no_results(async_client: AsyncClient):
    with patch_email_service():
        # Register and login first
        register_response = await async_client.post(
            "/api/auth/register",
            json={
                "email": "noresults@example.com",
                "password": "testpassword123",
                "confirm_password": "testpassword123",
                "full_name": "Test User"
            }
        )
        assert register_response.status_code == status.HTTP_201_CREATED
        
        # Verify email
        verification_token = auth_service.create_verification_token("noresults@example.com")
        await async_client.get(f"/api/auth/verify/{verification_token}")
        
        # Login
        login_response = await async_client.post(
            "/api/auth/login",
            data={
                "username": "noresults@example.com",
                "password": "testpassword123"
            }
        )
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.json()["access_token"]
        
        # Create a contact
        await async_client.post(
            "/api/contacts",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "phone": "+1234567890",
                "birthday": "1990-01-01",
                "notes": "Test contact"
            }
        )
        
        # Search for non-existent contact
        response = await async_client.get(
            "/api/contacts/search?query=Nonexistent",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

@pytest.mark.asyncio
async def test_search_contacts_unauthorized(async_client: AsyncClient):
    response = await async_client.get("/api/contacts/search?query=test")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert "detail" in data
    assert "not authenticated" in data["detail"].lower()

@pytest.mark.asyncio
async def test_rate_limit(async_client: AsyncClient):
    with patch_email_service():
        # Register and login first
        register_response = await async_client.post(
            "/api/auth/register",
            json={
                "email": "ratelimit@example.com",
                "password": "testpassword123",
                "confirm_password": "testpassword123",
                "full_name": "Test User"
            }
        )
        assert register_response.status_code == status.HTTP_201_CREATED
        
        # Verify email
        verification_token = auth_service.create_verification_token("ratelimit@example.com")
        await async_client.get(f"/api/auth/verify/{verification_token}")
        
        # Login
        login_response = await async_client.post(
            "/api/auth/login",
            data={
                "username": "ratelimit@example.com",
                "password": "testpassword123"
            }
        )
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.json()["access_token"]
        
        # Make multiple requests to test rate limiting
        for _ in range(6):
            response = await async_client.get(
                "/api/contacts",
                headers={"Authorization": f"Bearer {token}"}
            )
            if _ < 5:
                assert response.status_code == status.HTTP_200_OK
            else:
                assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS 