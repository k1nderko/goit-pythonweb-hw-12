from pydantic import BaseModel, EmailStr, Field, field_validator, field_serializer, ConfigDict
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str
    confirm_password: str

class UserResponse(UserBase):
    id: int
    is_verified: bool
    avatar: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: Optional[datetime] = None
    notes: Optional[str] = None

    @field_validator('birthday', mode='before')
    @classmethod
    def parse_birthday(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                raise ValueError('Invalid date format. Use YYYY-MM-DD')
        return value

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class ContactResponse(ContactBase):
    id: int
    owner_id: int

    @field_serializer('birthday')
    def serialize_birthday(self, birthday: Optional[datetime]) -> Optional[str]:
        if birthday:
            return birthday.strftime('%Y-%m-%d')
        return None

    model_config = ConfigDict(from_attributes=True)

from .auth import PasswordResetRequest, PasswordReset

__all__ = [
    'UserBase',
    'UserCreate',
    'UserResponse',
    'TokenResponse',
    'ContactBase',
    'ContactCreate',
    'ContactUpdate',
    'ContactResponse',
    'PasswordResetRequest',
    'PasswordReset'
] 