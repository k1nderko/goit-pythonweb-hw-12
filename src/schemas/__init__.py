from pydantic import BaseModel, EmailStr, Field, field_validator, field_serializer, ConfigDict
from typing import Optional, List
from datetime import datetime, UTC
from src.database.models import UserRole

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=100)
    confirm_password: str = Field(min_length=6, max_length=100)
    role: Optional[UserRole] = UserRole.USER

    def validate_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(UserBase):
    id: int
    role: UserRole
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[UserRole] = None

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
                dt = datetime.strptime(value, '%Y-%m-%d')
                return dt.replace(tzinfo=UTC)
            except ValueError:
                raise ValueError('Invalid date format. Use YYYY-MM-DD')
        return value if value is None or value.tzinfo is not None else value.replace(tzinfo=UTC)

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    birthday: Optional[datetime] = None
    notes: Optional[str] = None

class ContactResponse(ContactBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    @field_serializer('birthday')
    def serialize_birthday(self, birthday: Optional[datetime]) -> Optional[str]:
        if birthday:
            return birthday.strftime('%Y-%m-%d')
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