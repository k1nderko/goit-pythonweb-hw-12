"""
Database Models Module

This module defines the SQLAlchemy models for the application's database schema.
It includes models for users and their contacts, with proper relationships and constraints.

Models:
- User: Represents a user in the system with authentication and role management
- Contact: Represents a contact entry belonging to a user
- UserRole: Enum defining possible user roles (user, admin)

Each model includes:
- Primary keys and indexes
- Required and optional fields
- Relationships between models
- Timestamps for creation and updates
- Proper constraints and validations
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, UTC
from enum import Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

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
            role (UserRole): User's role (user or admin).
            contacts (List[Contact]): List of contacts associated with the user.
        """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(150), nullable=True)
    role = Column(SQLAlchemyEnum(UserRole), default=UserRole.USER, nullable=False)
    refresh_token = Column(String(255), nullable=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

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
    birthday = Column(DateTime(timezone=True), nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="contacts")
