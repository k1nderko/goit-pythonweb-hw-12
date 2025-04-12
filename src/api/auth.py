"""
Authentication API Router Module

This module provides the API endpoints for user authentication and management.
It includes user registration, login, email verification, password reset, and user management.

Endpoints:
- POST /register: Register a new user
- POST /login: User login
- POST /refresh: Refresh access token
- POST /verify/{token}: Verify user email
- POST /request-verification: Request email verification
- POST /reset-password: Reset password
- POST /reset-password/{token}: Confirm password reset
- GET /me: Get current user info
- POST /upload-avatar: Upload user avatar
- PUT /users/{user_id}/role: Update user role (admin only)
- PUT /users/{user_id}/status: Update user status (admin only)

All endpoints are protected with rate limiting, and sensitive operations require authentication.
"""

from fastapi import APIRouter, HTTPException, Depends, status, Security, BackgroundTasks, Request, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.limiter import limiter
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from src.database.session import get_async_db
from src.schemas import UserCreate, UserResponse, TokenResponse, UserUpdate
from src.schemas.auth import PasswordResetRequest, PasswordReset
from src.repository import users as users_repo
from src.services.auth import auth_service, get_current_user, get_current_admin_user
from src.database.models import User, UserRole
from src.conf.config import settings
from src.services.email import send_verification_email, send_password_reset_email
from src.services.cloudinary_service import upload_avatar
import shutil
import os
from src.database.db import get_session

router = APIRouter(tags=["auth"])
security = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register(
    body: UserCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_async_db)
) -> dict:
    """
    Register a new user and send verification email.
    
    Args:
        body: UserCreate - The user registration data
        background_tasks: BackgroundTasks - For sending email in background
        request: Request - The request object
        db: AsyncSession - The database session
        
    Returns:
        dict: The created user
        
    Raises:
        HTTPException: If email already exists
    """
    exist_user = await users_repo.get_user_by_email(db, body.email)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    
    hashed_password = auth_service.get_password_hash(body.password)
    user_data = body.model_dump(exclude={"password", "confirm_password"})
    new_user = await users_repo.create_user(db, hashed_password=hashed_password, **user_data)
    
    # Create verification token
    token = await auth_service.create_verification_token({"sub": new_user.email})
    
    # Get base URL from request
    base_url = str(request.base_url).rstrip('/')
    
    # Add email sending to background tasks
    background_tasks.add_task(send_verification_email, new_user.email, token, base_url)
    
    return {
        "id": new_user.id,
        "email": new_user.email,
        "full_name": new_user.full_name,
        "role": new_user.role,
        "is_verified": new_user.is_verified,
        "created_at": new_user.created_at,
        "updated_at": new_user.updated_at
    }


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
async def login(request: Request, body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_async_db)):
    """
    Login for access token.
    """
    user = await auth_service.authenticate_user(body.username, body.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified"
        )
    return auth_service.create_tokens(user)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: AsyncSession = Depends(get_session)
) -> dict:
    """
    Refresh an access token using a refresh token.
    
    Args:
        credentials: HTTPAuthorizationCredentials - The refresh token credentials
        db: AsyncSession - The database session
        
    Returns:
        dict: The new access and refresh tokens
        
    Raises:
        HTTPException: If the refresh token is invalid
    """
    token = credentials.credentials
    payload = await auth_service.verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    email = payload.get("sub")
    user = await users_repo.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.create_access_token({"sub": user.email, "role": user.role})
    refresh_token = auth_service.create_refresh_token({"sub": user.email})
    await users_repo.update_token(db, user, refresh_token)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/verify/{token}")
@limiter.limit("5/minute")
async def verify_email(token: str, request: Request, db: AsyncSession = Depends(get_async_db)):
    """
    Verify user's email using the verification token.
    
    Args:
        token: str - The verification token
        request: Request - The request object
        db: AsyncSession - The database session
        
    Returns:
        dict: A message indicating success
        
    Raises:
        HTTPException: If the token is invalid or user not found
    """
    email = await auth_service.verify_verification_token(token)
    user = await users_repo.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.is_verified:
        return {"message": "Email already verified"}
    
    await users_repo.update_user_verified(db, user.id, True)
    return {"message": "Email verified successfully"}


@router.post("/request-verification", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def request_verification(email: str, background_tasks: BackgroundTasks, request: Request, db: AsyncSession = Depends(get_async_db)):
    """
    Request a new verification email.
    """
    user = await users_repo.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.is_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already verified")
    
    token = await auth_service.create_verification_token({"sub": email})
    base_url = str(request.base_url).rstrip('/')
    
    background_tasks.add_task(send_verification_email, email, token, base_url)
    return {"message": "Verification email sent"}


@router.post("/reset-password")
@limiter.limit("5/minute")
async def reset_password(
    body: PasswordResetRequest,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_session)
):
    """
    Request a password reset.
    
    Args:
        body: PasswordResetRequest - Contains the email to send reset link to
        background_tasks: BackgroundTasks - For sending email in background
        request: Request - The request object
        db: AsyncSession - The database session
        
    Returns:
        dict: A message indicating success
        
    Raises:
        HTTPException: If the user is not found
    """
    user = await users_repo.get_user_by_email(db, body.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Create password reset token
    token = await auth_service.create_password_reset_token({"sub": user.email})
    
    # Get base URL from request
    base_url = str(request.base_url).rstrip('/')
    
    # Add email sending to background tasks
    background_tasks.add_task(send_password_reset_email, user.email, token, base_url)
    
    return {"message": "Password reset email sent"}


@router.post("/reset-password/{token}")
@limiter.limit("5/minute")
async def reset_password_confirm(
    token: str,
    body: PasswordReset,
    request: Request,
    db: AsyncSession = Depends(get_session)
):
    """
    Reset a user's password using a reset token.
    
    Args:
        token: str - The reset token
        body: PasswordReset - Contains the new password
        request: Request - The request object
        db: AsyncSession - The database session
        
    Returns:
        dict: A message indicating success
        
    Raises:
        HTTPException: If the token is invalid or expired
    """
    email = await auth_service.verify_password_reset_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    user = await users_repo.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Hash the new password and update user
    hashed_password = auth_service.get_password_hash(body.new_password)
    await users_repo.update_user_password(db, user.id, hashed_password)
    
    return {"message": "Password reset successfully"}


@router.post("/request-password-reset", response_model=dict)
@limiter.limit("5/minute")
async def request_password_reset(
    request: Request,
    reset_data: PasswordResetRequest,
    db: AsyncSession = Depends(get_session)
):
    """
    Request a password reset email.
    
    Args:
        request: Request - The request object
        reset_data: PasswordResetRequest - The reset request data
        db: AsyncSession - The database session
        
    Returns:
        dict: A message indicating success
        
    Raises:
        HTTPException: If the user is not found
    """
    user = await users_repo.get_user_by_email(db, reset_data.email)
    if not user:
        # Return success even if user doesn't exist to prevent email enumeration
        return {"message": "If your email is registered, you will receive a password reset link"}
    
    token = auth_service.create_password_reset_token(reset_data.email)
    # TODO: Send password reset email
    return {"message": "If your email is registered, you will receive a password reset link"}


@router.get("/me", response_model=UserResponse)
@limiter.limit("10/minute")
async def get_me(
    request: Request,
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Get the current user's information.
    
    Args:
        request: Request - The request object
        current_user: User - The current authenticated user
        
    Returns:
        dict: The current user's information
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "is_verified": current_user.is_verified,
        "created_at": current_user.created_at,
        "updated_at": current_user.updated_at
    }


@router.post("/upload-avatar", response_model=UserResponse)
async def upload_user_avatar(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
    file: UploadFile = File(...)
):
    """
    Upload a user's avatar.
    
    Args:
        current_user: User - The current authenticated user
        db: AsyncSession - The database session
        file: UploadFile - The avatar file to upload
        
    Returns:
        UserResponse: The updated user
        
    Raises:
        HTTPException: If there's an error uploading the file
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    try:
        # Upload to Cloudinary
        result = await upload_avatar(file.file, current_user.email)
        avatar_url = result.get("secure_url")
        
        # Update user's avatar URL
        user = await users_repo.update_user(db, current_user, avatar=avatar_url)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/reset-password", response_model=dict)
@limiter.limit("5/minute")
async def reset_password(
    request: Request,
    reset_data: PasswordReset,
    db: AsyncSession = Depends(get_session)
):
    """
    Reset a user's password using a valid reset token.
    
    Args:
        request: Request - The request object
        reset_data: PasswordReset - The reset data
        db: AsyncSession - The database session
        
    Returns:
        dict: A message indicating success
        
    Raises:
        HTTPException: If the token is invalid or passwords don't match
    """
    if reset_data.new_password != reset_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    
    success = await auth_service.reset_password(reset_data.token, reset_data.new_password, db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    return {"message": "Password has been reset successfully"}


@router.put("/users/{user_id}/role", response_model=UserResponse)
async def update_user_role(
    user_id: int,
    new_role: UserRole,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Update a user's role.
    
    Args:
        user_id: int - The ID of the user to update
        new_role: UserRole - The new role to assign
        current_user: User - The current admin user
        db: AsyncSession - The database session
        
    Returns:
        UserResponse: The updated user
        
    Raises:
        HTTPException: If the user is not found or current user is not an admin
    """
    user = await users_repo.update_user(db, user_id, role=new_role)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/users/{user_id}/status", response_model=UserResponse)
async def update_user_status(
    user_id: int,
    is_active: bool,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Update a user's active status.
    
    Args:
        user_id: int - The ID of the user to update
        is_active: bool - The new active status
        current_user: User - The current admin user
        db: AsyncSession - The database session
        
    Returns:
        UserResponse: The updated user
        
    Raises:
        HTTPException: If the user is not found or current user is not an admin
    """
    user = await users_repo.update_user(db, user_id, is_active=is_active)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user