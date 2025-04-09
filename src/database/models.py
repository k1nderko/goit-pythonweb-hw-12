from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.database.db import Base
from typing import Optional

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
            contacts (List[Contact]): List of contacts associated with the user.
        """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    avatar: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    contacts = relationship("Contact", back_populates="owner")

class Contact(Base):
    """
        SQLAlchemy model representing a contact belonging to a user.

        Attributes:
            id (int): Unique identifier for the contact.
            first_name (str): First name of the contact.
            last_name (str): Last name of the contact.
            email (str): Email address of the contact.
            phone_number (str): Phone number of the contact.
            birth_date (date): Birth date of the contact.
            additional_info (Optional[str]): Any additional information about the contact.
            owner_id (int): Foreign key to the associated user.
            owner (User): The user who owns this contact.
        """
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    additional_info = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="contacts")
