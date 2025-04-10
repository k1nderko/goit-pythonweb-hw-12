from datetime import date
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=50)

class UserCreate(UserBase):
    password: str = Field(min_length=6)
    confirm_password: str = Field(min_length=6)

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    avatar: str | None = None

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class ContactBase(BaseModel):
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    phone: str = Field(pattern=r"^\+?1?\d{9,15}$")
    birthday: date
    notes: str | None = None

class ContactCreate(ContactBase):
    pass

class ContactResponse(ContactBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class ContactUpdate(ContactBase):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    birthday: date | None = None
    notes: str | None = None
