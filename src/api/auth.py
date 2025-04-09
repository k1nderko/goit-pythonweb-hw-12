from fastapi import APIRouter, Depends, HTTPException, status, Request, File, UploadFile
from src.services.limiter import limiter
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from src.database.db import get_db
from src.schemas import UserCreate, UserResponse, Token
from src.repository.users import create_user, get_user_by_email, verify_user_email
from src.services.auth import verify_password, create_access_token
from src.database.models import User
from src.services.auth import SECRET_KEY, ALGORITHM
from src.conf.mail import send_verification_email
from src.services.cloudinary_service import upload_avatar
import shutil
import os

router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
        Sign up a new user and send an email verification link.

        Args:
            user_data (UserCreate): The user's email and password for registration.
            db (Session): Database session.

        Returns:
            UserResponse: The created user object.
        """
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = create_user(db, user_data)

    token = create_access_token(data={"sub": user.email})

    await send_verification_email(user.email, token)

    return user


@router.get("/verify-email/{token}")
async def verify_email(token: str, db: Session = Depends(get_db)):
    """
        Verify the email address by decoding the token.

        Args:
            token (str): The email verification token.
            db (Session): Database session.

        Returns:
            dict: A message indicating the email verification status.
        """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

        user = get_user_by_email(db, email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        verify_user_email(db, email)

        return {"message": "Email successfully verified"}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
        Log in an existing user by verifying credentials and returning a JWT access token.

        Args:
            form_data (OAuth2PasswordRequestForm): The form containing username and password.
            db (Session): Database session.

        Returns:
            Token: JWT access token for authenticated users.
        """
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email not verified")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
        Retrieve the current user by decoding the JWT token.

        Args:
            db (Session): Database session.
            token (str): JWT token.

        Returns:
            User: The user associated with the token.

        Raises:
            HTTPException: If the token is invalid or user is not found.
        """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

        user = get_user_by_email(db, email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

        if not user.is_verified:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email not verified")

        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

@router.get("/me", response_model=UserResponse)
@limiter.limit("5/minute")
async def read_current_user(request: Request, current_user: User = Depends(get_current_user)):
    """
        Retrieve the current logged-in user's details.

        Args:
            request (Request): The incoming request.
            current_user (User): The current authenticated user.

        Returns:
            UserResponse: The user's profile information.
        """
    return current_user

@router.post("/upload-avatar", response_model=UserResponse)
async def upload_user_avatar(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
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