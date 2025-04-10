from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    """
        SQLAlchemy model representing a user.

        Attributes:
            id (int): Unique identifier for the user.
            email (str): Unique email address of the user.
            hashed_password (str): Hashed password for authentication.
            is_active (bool): Flag indicating if the user is active.
            is_verified (bool): Flag indicating if the user's email is verified.
            avatar (Optional[str]): URL or path to the user's avatar image.
            full_name (str): Full name of the user.
            contacts (List[Contact]): List of contacts associated with the user.
        """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    avatar = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    contacts = relationship("Contact", back_populates="owner", cascade="all, delete-orphan")

class Contact(Base):
    """
        SQLAlchemy model representing a contact belonging to a user.

        Attributes:
            id (int): Unique identifier for the contact.
            first_name (str): First name of the contact.
            last_name (str): Last name of the contact.
            email (str): Email address of the contact (unique per user).
            phone_number (str): Phone number of the contact.
            birth_date (date): Birth date of the contact.
            additional_info (Optional[str]): Any additional information about the contact.
            owner_id (int): Foreign key to the associated user.
            owner (User): The user who owns this contact.
        """
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    birthday = Column(DateTime, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="contacts")
