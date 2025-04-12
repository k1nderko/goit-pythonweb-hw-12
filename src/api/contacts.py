"""
Contacts API Router Module

This module provides the API endpoints for managing contacts in the application.
It includes CRUD operations for contacts with rate limiting and authentication.

Endpoints:
- POST /: Create a new contact
- GET /: List all contacts for the current user
- GET /search: Search contacts by name or email
- GET /{contact_id}: Get a specific contact
- PUT /{contact_id}: Update a contact
- DELETE /{contact_id}: Delete a contact

All endpoints are protected with authentication and rate limiting.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.database.session import get_async_db
from src.schemas import ContactCreate, ContactResponse, ContactUpdate
from src.repository import contacts as contacts_repo
from src.services.auth import get_current_user
from src.services.limiter import limiter

router = APIRouter(tags=["contacts"])

@router.post("/", response_model=ContactResponse, status_code=201)
@limiter.limit("5/minute")
async def create_contact(
    request: Request,
    contact: ContactCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_user)
):
    """
    Create a new contact.
    
    Args:
        request: Request - The request object
        contact: ContactCreate - The contact data to create
        db: AsyncSession - The database session
        current_user: User - The current authenticated user
        
    Returns:
        ContactResponse: The created contact
    """
    return await contacts_repo.create_contact(db, contact, current_user.id)

@router.get("/", response_model=List[ContactResponse])
@limiter.limit("5/minute")
async def get_contacts(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_user)
):
    """
    Get all contacts for the current user.
    
    Args:
        request: Request - The request object
        skip: int - Number of contacts to skip
        limit: int - Maximum number of contacts to return
        db: AsyncSession - The database session
        current_user: User - The current authenticated user
        
    Returns:
        List[ContactResponse]: List of contacts
    """
    return await contacts_repo.get_contacts(db, current_user.id, skip, limit)

@router.get("/search", response_model=List[ContactResponse])
@limiter.limit("5/minute")
async def search_contacts(
    request: Request,
    query: str = Query(..., min_length=1, description="Search query for name or email"),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_user)
):
    """
    Search for contacts by name or email.
    
    Args:
        request: Request - The request object
        query: str - The search query
        db: AsyncSession - The database session
        current_user: User - The current authenticated user
        
    Returns:
        List[ContactResponse]: List of matching contacts
    """
    return await contacts_repo.search_contacts(db, current_user.id, query)

@router.get("/{contact_id}", response_model=ContactResponse)
@limiter.limit("5/minute")
async def get_contact(
    request: Request,
    contact_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_user)
):
    """
    Get a contact by ID.
    
    Args:
        request: Request - The request object
        contact_id: int - The ID of the contact
        db: AsyncSession - The database session
        current_user: User - The current authenticated user
        
    Returns:
        ContactResponse: The contact
        
    Raises:
        HTTPException: If the contact is not found
    """
    contact = await contacts_repo.get_contact(db, contact_id, current_user.id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=ContactResponse)
@limiter.limit("5/minute")
async def update_contact(
    request: Request,
    contact_id: int,
    contact: ContactUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_user)
):
    """
    Update a contact.
    
    Args:
        request: Request - The request object
        contact_id: int - The ID of the contact
        contact: ContactUpdate - The contact data to update
        db: AsyncSession - The database session
        current_user: User - The current authenticated user
        
    Returns:
        ContactResponse: The updated contact
        
    Raises:
        HTTPException: If the contact is not found
    """
    updated_contact = await contacts_repo.update_contact(db, contact_id, contact, current_user.id)
    if not updated_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("5/minute")
async def delete_contact(
    request: Request,
    contact_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_user)
):
    """
    Delete a contact.
    
    Args:
        request: Request - The request object
        contact_id: int - The ID of the contact
        db: AsyncSession - The database session
        current_user: User - The current authenticated user
        
    Returns:
        None: The response code indicating the contact was deleted
        
    Raises:
        HTTPException: If the contact is not found
    """
    deleted_contact = await contacts_repo.delete_contact(db, contact_id, current_user.id)
    if not deleted_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return None
