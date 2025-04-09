from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.schemas import ContactCreate, ContactUpdate, ContactResponse
from src.repository.contacts import create_contact, get_contacts, get_contact, update_contact, delete_contact
from src.api.auth import get_current_user
from src.database.models import User

router = APIRouter(prefix="/contacts", tags=["Contacts"])

@router.post("/", response_model=ContactResponse)
def add_contact(contact: ContactCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
        Add a new contact to the user's contact list.

        Args:
            contact (ContactCreate): The contact's details to be added.
            db (Session): Database session.
            current_user (User): The current logged-in user.

        Returns:
            ContactResponse: The newly added contact.
        """
    return create_contact(db, contact, current_user)

@router.get("/", response_model=list[ContactResponse])
def list_contacts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
        Retrieve all contacts for the current user.

        Args:
            db (Session): Database session.
            current_user (User): The current logged-in user.

        Returns:
            list[ContactResponse]: The list of user's contacts.
        """
    return get_contacts(db, user_id=current_user.id)

@router.get("/{contact_id}", response_model=ContactResponse)
def read_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
        Retrieve a specific contact by ID.

        Args:
            contact_id (int): The ID of the contact to retrieve.
            db (Session): Database session.
            current_user (User): The current logged-in user.

        Returns:
            ContactResponse: The requested contact.

        Raises:
            HTTPException: If the contact is not found.
        """
    contact = get_contact(db, contact_id, current_user.id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=ContactResponse)
def edit_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
        Edit the details of an existing contact.

        Args:
            contact_id (int): The ID of the contact to edit.
            contact (ContactUpdate): The updated contact information.
            db (Session): Database session.
            current_user (User): The current logged-in user.

        Returns:
            ContactResponse: The updated contact.

        Raises:
            HTTPException: If the contact is not found.
        """
    updated_contact = update_contact(db, contact_id, contact, current_user.id)
    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact

@router.delete("/{contact_id}", response_model=ContactResponse)
def remove_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
        Delete a contact from the user's contact list.

        Args:
            contact_id (int): The ID of the contact to remove.
            db (Session): Database session.
            current_user (User): The current logged-in user.

        Returns:
            ContactResponse: The deleted contact.

        Raises:
            HTTPException: If the contact is not found.
        """
    deleted_contact = delete_contact(db, contact_id, current_user.id)
    if deleted_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return deleted_contact
