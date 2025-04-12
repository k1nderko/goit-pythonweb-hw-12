"""
Application Schema Module

This module defines Pydantic models for data validation and serialization.
It includes models for users, contacts, and authentication tokens.

The schemas are used to:
- Validate incoming request data
- Serialize outgoing response data
- Define API documentation
"""

from pydantic import BaseModel, EmailStr, Field, field_validator, field_serializer, ConfigDict
from typing import Optional, List
from datetime import datetime, UTC
from src.database.models import UserRole

class UserBase(BaseModel):
    """
    Base schema for user data.
    
    Attributes:
        email: The user's email address
        full_name: The user's full name (optional)
    """
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    """
    Schema for creating a new user.
    
    Attributes:
        email: The user's email address
        full_name: The user's full name (optional)
        password: The user's password (6-100 characters)
        confirm_password: Confirmation of the password
        role: The user's role (defaults to USER)
    """
    password: str = Field(min_length=6, max_length=100)
    confirm_password: str = Field(min_length=6, max_length=100)
    role: Optional[UserRole] = UserRole.USER

    def validate_passwords_match(self):
        """
        Validate that the password and confirmation match.
        
        Returns:
            bool: True if passwords match
            
        Raises:
            ValueError: If passwords do not match
        """
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return True

class UserUpdate(BaseModel):
    """
    Schema for updating a user.
    
    Attributes:
        full_name: The user's full name (optional)
        email: The user's email address (optional)
    """
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(UserBase):
    """
    Schema for user response data.
    
    Attributes:
        id: The user's ID
        email: The user's email address
        full_name: The user's full name
        role: The user's role
        is_verified: Whether the user's email is verified
        created_at: When the user was created
        updated_at: When the user was last updated
    """
    id: int
    role: UserRole
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class TokenResponse(BaseModel):
    """
    Schema for authentication token response.
    
    Attributes:
        access_token: The JWT access token
        refresh_token: The JWT refresh token
        token_type: The token type (always "bearer")
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class TokenData(BaseModel):
    """
    Schema for token payload data.
    
    Attributes:
        email: The user's email (optional)
        role: The user's role (optional)
    """
    email: Optional[str] = None
    role: Optional[UserRole] = None

class ContactBase(BaseModel):
    """
    Base schema for contact data.
    
    Attributes:
        first_name: The contact's first name
        last_name: The contact's last name
        email: The contact's email address
        phone: The contact's phone number
        birthday: The contact's birthday (optional)
        notes: Additional notes about the contact (optional)
    """
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: Optional[datetime] = None
    notes: Optional[str] = None

    @field_validator('birthday', mode='before')
    @classmethod
    def parse_birthday(cls, value):
        """
        Parse birthday string to datetime.
        
        Args:
            value: The birthday value to parse
            
        Returns:
            datetime: The parsed datetime or None
        """
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                return None
        return value

class ContactCreate(ContactBase):
    """
    Schema for creating a new contact.
    
    Inherits all attributes from ContactBase.
    """
    pass

class ContactUpdate(BaseModel):
    """
    Schema for updating a contact.
    
    All fields are optional to allow partial updates.
    
    Attributes:
        first_name: The contact's first name (optional)
        last_name: The contact's last name (optional)
        email: The contact's email address (optional)
        phone: The contact's phone number (optional)
        birthday: The contact's birthday (optional)
        notes: Additional notes about the contact (optional)
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    birthday: Optional[datetime] = None
    notes: Optional[str] = None

class ContactResponse(ContactBase):
    """
    Schema for contact response data.
    
    Inherits all attributes from ContactBase and adds:
    
    Attributes:
        id: The contact's ID
        owner_id: The ID of the user who owns this contact
        created_at: When the contact was created
        updated_at: When the contact was last updated
    """
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    @field_serializer('birthday')
    def serialize_birthday(self, birthday: Optional[datetime]) -> Optional[str]:
        """
        Serialize birthday datetime to ISO format string.
        
        Args:
            birthday: The birthday datetime to serialize
            
        Returns:
            str: The ISO format string or None
        """
        if birthday:
            return birthday.isoformat()
        return None
    
    class Config:
        from_attributes = True

from .auth import PasswordResetRequest, PasswordReset

__all__ = [
    'UserBase',
    'UserCreate',
    'UserUpdate',
    'UserResponse',
    'TokenResponse',
    'TokenData',
    'ContactBase',
    'ContactCreate',
    'ContactUpdate',
    'ContactResponse',
    'PasswordResetRequest',
    'PasswordReset'
] 