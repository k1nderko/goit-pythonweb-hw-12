"""
Authentication Schema Module

This module defines Pydantic models for authentication-related operations,
including password reset requests and confirmations.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class PasswordResetRequest(BaseModel):
    """
    Schema for requesting a password reset.
    
    Attributes:
        email: The email address of the user requesting a password reset
    """
    email: EmailStr

class PasswordReset(BaseModel):
    """
    Schema for resetting a password.
    
    Attributes:
        token: The password reset token received via email
        new_password: The new password (minimum 8 characters)
        confirm_password: Confirmation of the new password
    """
    token: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8) 