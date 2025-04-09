from sqlalchemy.orm import Session
from src.database.models import Contact, User
from src.schemas import ContactCreate, ContactUpdate

def create_contact(db: Session, contact: ContactCreate, user: User):
    """
        Create a new contact and associate it with the given user.

        Args:
            db (Session): Database session.
            contact (ContactCreate): The contact details to be added.
            user (User): The user to whom the contact belongs.

        Returns:
            Contact: The newly created contact.
        """
    db_contact = Contact(**contact.dict(), owner_id=user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contacts(db: Session, user_id: int):
    """
        Retrieve all contacts for a specific user.

        Args:
            db (Session): Database session.
            user_id (int): The ID of the user.

        Returns:
            list[Contact]: The list of contacts.
        """
    return db.query(Contact).filter(Contact.owner_id == user_id).all()

def get_contact(db: Session, contact_id: int, user_id: int):
    """
        Retrieve a specific contact for a given user.

        Args:
            db (Session): Database session.
            contact_id (int): The ID of the contact.
            user_id (int): The ID of the user.

        Returns:
            Contact: The requested contact.

        Raises:
            HTTPException: If the contact is not found.
        """
    return db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == user_id).first()

def update_contact(db: Session, contact_id: int, contact: ContactUpdate, user_id: int):
    """
        Update a contact's details for a specific user.

        Args:
            db (Session): Database session.
            contact_id (int): The ID of the contact to update.
            contact (ContactUpdate): The updated contact details.
            user_id (int): The ID of the user.

        Returns:
            Contact: The updated contact.

        Raises:
            HTTPException: If the contact is not found.
        """
    db_contact = db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == user_id).first()
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int, user_id: int):
    """
        Delete a contact for a specific user.

        Args:
            db (Session): Database session.
            contact_id (int): The ID of the contact to delete.
            user_id (int): The ID of the user.

        Returns:
            Contact: The deleted contact.

        Raises:
            HTTPException: If the contact is not found.
        """
    db_contact = db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == user_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact
