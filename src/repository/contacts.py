"""
Contact repository for database operations.

This module provides functions for CRUD operations on contacts,
including search functionality.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from src.database.models import Contact, User
from src.schemas import ContactCreate, ContactUpdate

async def create_contact(db: AsyncSession, contact: ContactCreate, user_id: int) -> Contact:
    """
    Create a new contact.
    
    Args:
        db: AsyncSession - The database session
        contact: ContactCreate - The contact data to create
        user_id: int - The ID of the user creating the contact
        
    Returns:
        Contact: The created contact
    """
    db_contact = Contact(
        **contact.model_dump(),
        owner_id=user_id
    )
    db.add(db_contact)
    await db.commit()
    await db.refresh(db_contact)
    return db_contact

async def get_contacts(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> list[Contact]:
    """
    Get all contacts for a user with pagination.
    
    Args:
        db: AsyncSession - The database session
        user_id: int - The ID of the user
        skip: int - Number of contacts to skip (for pagination)
        limit: int - Maximum number of contacts to return
        
    Returns:
        list[Contact]: List of contacts belonging to the user
    """
    result = await db.execute(
        select(Contact)
        .where(Contact.owner_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_contact(db: AsyncSession, contact_id: int, user_id: int) -> Contact | None:
    """
    Get a specific contact by ID.
    
    Args:
        db: AsyncSession - The database session
        contact_id: int - The ID of the contact to retrieve
        user_id: int - The ID of the user who owns the contact
        
    Returns:
        Contact | None: The contact if found, None otherwise
    """
    result = await db.execute(
        select(Contact)
        .where(Contact.id == contact_id)
        .where(Contact.owner_id == user_id)
    )
    return result.scalar_one_or_none()

async def update_contact(db: AsyncSession, contact_id: int, contact: ContactUpdate, user_id: int) -> Contact | None:
    """
    Update a contact's information.
    
    Args:
        db: AsyncSession - The database session
        contact_id: int - The ID of the contact to update
        contact: ContactUpdate - The updated contact data
        user_id: int - The ID of the user who owns the contact
        
    Returns:
        Contact | None: The updated contact if found, None otherwise
    """
    db_contact = await get_contact(db, contact_id, user_id)
    if not db_contact:
        return None
        
    for key, value in contact.model_dump(exclude_unset=True).items():
        setattr(db_contact, key, value)
        
    await db.commit()
    await db.refresh(db_contact)
    return db_contact

async def delete_contact(db: AsyncSession, contact_id: int, user_id: int) -> Contact | None:
    """
    Delete a contact.
    
    Args:
        db: AsyncSession - The database session
        contact_id: int - The ID of the contact to delete
        user_id: int - The ID of the user who owns the contact
        
    Returns:
        Contact | None: The deleted contact if found, None otherwise
    """
    db_contact = await get_contact(db, contact_id, user_id)
    if not db_contact:
        return None
        
    await db.delete(db_contact)
    await db.commit()
    return db_contact

async def search_contacts(db: AsyncSession, user_id: int, query: str) -> list[Contact]:
    """
    Search for contacts by name or email.
    
    Args:
        db: AsyncSession - The database session
        user_id: int - The ID of the user who owns the contacts
        query: str - The search query to match against names or email
        
    Returns:
        list[Contact]: List of contacts matching the search query
    """
    result = await db.execute(
        select(Contact)
        .where(Contact.owner_id == user_id)
        .where(
            or_(
                Contact.first_name.ilike(f"%{query}%"),
                Contact.last_name.ilike(f"%{query}%"),
                Contact.email.ilike(f"%{query}%")
            )
        )
    )
    contacts = result.scalars().all()
    # Ensure each contact has the owner_id field set
    for contact in contacts:
        contact.owner_id = user_id
    return contacts
