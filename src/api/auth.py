from fastapi import APIRouter, HTTPException, Depends, status, Security, BackgroundTasks, Request, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.limiter import limiter
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from src.database.session import get_async_db
from src.schemas import UserCreate, UserResponse, TokenResponse
from src.repository import users as users_repo
from src.services.auth import auth_service
from src.database.models import User
from src.conf.config import settings
from src.services.email import send_verification_email
from src.services.cloudinary_service import upload_avatar
import shutil
import os

router = APIRouter(tags=["auth"])
security = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register(
    request: Request,
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Register a new user.
    
    Args:
        request: Request - The request object
        user: UserCreate - The user data to create
        background_tasks: BackgroundTasks - For sending verification email
        db: AsyncSession - The database session
        
    Returns:
        UserResponse: The created user
        
    Raises:
        HTTPException: If the email is already registered
    """
    existing_user = await users_repo.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    db_user = await users_repo.create_user(db, user)
    
    # Generate verification token and send email
    verification_token = auth_service.create_verification_token(user.email)
    background_tasks.add_task(send_verification_email, user.email, verification_token)
    
    return db_user


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Login a user.
    
    Args:
        request: Request - The request object
        form_data: OAuth2PasswordRequestForm - The login credentials
        db: AsyncSession - The database session
        
    Returns:
        TokenResponse: The access and refresh tokens
        
    Raises:
        HTTPException: If the credentials are invalid or email is not verified
    """
    user = await users_repo.get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    if not auth_service.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified"
        )
    
    # Generate access and refresh tokens
    access_token = auth_service.create_access_token({"sub": user.email})
    refresh_token = auth_service.create_refresh_token({"sub": user.email})
    
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get("/verify/{token}", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def verify_email(
    request: Request,
    token: str,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Verify a user's email.
    
    Args:
        request: Request - The request object
        token: str - The verification token
        db: AsyncSession - The database session
        
    Returns:
        dict: A success message
        
    Raises:
        HTTPException: If the token is invalid or expired
    """
    email = auth_service.verify_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )
    
    user = await users_repo.verify_user_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "Email verified successfully"}


@router.get("/me", response_model=UserResponse)
@limiter.limit("10/minute")
async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get the current authenticated user.
    
    Args:
        request: Request - The request object
        credentials: HTTPAuthorizationCredentials - The bearer token
        db: AsyncSession - The database session
        
    Returns:
        UserResponse: The current user
        
    Raises:
        HTTPException: If the token is invalid or user not found
    """
    token = credentials.credentials
    email = auth_service.verify_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user = await users_repo.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.post("/upload-avatar", response_model=UserResponse)
async def upload_user_avatar(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_async_db),
    file: UploadFile = File(...)
):
    """
        Upload and update the user's avatar.

        Args:
            current_user (User): The current logged-in user.
            db (Session): Database session.
            file (UploadFile): The avatar file to be uploaded.

        Returns:
            UserResponse: The updated user with the avatar URL.
        """
    print("Upload endpoint triggered")
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    avatar_url = upload_avatar(temp_file_path, public_id=f"user_{current_user.id}")

    os.remove(temp_file_path)

    current_user.avatar = avatar_url
    db.commit()
    db.refresh(current_user)

    return current_user