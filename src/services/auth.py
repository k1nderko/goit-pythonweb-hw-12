from datetime import datetime, timedelta, UTC
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from src.conf.config import settings
from src.database.session import get_async_db
from src.repository import users as repository_users
from src.utils.password import verify_password, get_password_hash
from src.database.models import User, UserRole
from src.schemas import UserCreate, UserUpdate, TokenResponse, TokenData, UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS
        self.verification_token_expire_hours = 24
        self.reset_token_expire_minutes = 15

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against a hashed password.
        
        Args:
            plain_password: str - The plain text password
            hashed_password: str - The hashed password to compare against
            
        Returns:
            bool: True if the passwords match, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """
        Get a hashed password from a plain password.
        
        Args:
            password: str - The plain text password
            
        Returns:
            str: The hashed password
        """
        return pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create an access token.
        
        Args:
            data: dict - The data to encode in the token
            expires_delta: Optional[timedelta] - The expiration time for the token
            
        Returns:
            str: The encoded JWT token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire, "type": "access"})
        token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return token

    def create_refresh_token(self, data: dict) -> str:
        """
        Create a refresh token.
        
        Args:
            data: dict - The data to encode in the token
            
        Returns:
            str: The encoded JWT token
        """
        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({"exp": expire, "type": "refresh"})
        token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return token

    async def create_verification_token(self, data: dict) -> str:
        """
        Create an email verification token.
        
        Args:
            data: dict - The data to encode in the token
            
        Returns:
            str: The encoded JWT token
        """
        email = data.get("sub")
        if not email:
            raise ValueError("Email is required for verification token")
            
        to_encode = {
            "sub": email,
            "exp": datetime.now(UTC) + timedelta(hours=self.verification_token_expire_hours),
            "type": "verification"
        }
        token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return token

    def verify_token(self, token: str) -> dict:
        """
        Verify a JWT token.
        
        Args:
            token: str - The token to verify
            
        Returns:
            dict: The decoded payload from the token
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None

    async def get_current_user(self, token: str, db: AsyncSession) -> User:
        """
        Get the current authenticated user.
        
        Args:
            token: str - The JWT token from the request
            db: AsyncSession - The database session
            
        Returns:
            User: The current authenticated user
            
        Raises:
            HTTPException: If the token is invalid or the user is not found
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            # Decode JWT
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        user = await repository_users.get_user_by_email(db, email)
        if user is None:
            raise credentials_exception
        return user

    def create_password_reset_token(self, email: str) -> str:
        """
        Create a password reset token.
        
        Args:
            email: str - The email to encode in the token
            
        Returns:
            str: The encoded JWT token
        """
        to_encode = {"sub": email, "type": "password_reset"}
        expire = datetime.now(UTC) + timedelta(hours=1)  # Token expires in 1 hour
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return token

    def verify_password_reset_token(self, token: str) -> Optional[str]:
        """
        Verify a password reset token.
        
        Args:
            token: str - The token to verify
            
        Returns:
            Optional[str]: The email from the token if valid, None otherwise
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            email: str = payload.get("sub")
            token_type: str = payload.get("type")
            if email is None or token_type != "password_reset":
                return None
            return email
        except JWTError:
            return None

    async def reset_password(self, token: str, new_password: str, db: AsyncSession) -> bool:
        """
        Reset a user's password using a valid reset token.
        
        Args:
            token: str - The password reset token
            new_password: str - The new password to set
            db: AsyncSession - Database session
            
        Returns:
            bool: True if password was reset successfully, False otherwise
        """
        email = self.verify_password_reset_token(token)
        if not email:
            return False
            
        user = await repository_users.get_user_by_email(db, email)
        if not user:
            return False
            
        hashed_password = self.get_password_hash(new_password)
        user.hashed_password = hashed_password
        await db.commit()
        return True

    async def authenticate_user(self, email: str, password: str, db: AsyncSession) -> Optional[User]:
        """
        Authenticate a user with email and password.
        
        Args:
            email: str - User's email
            password: str - User's password
            db: AsyncSession - Database session
            
        Returns:
            Optional[User]: The authenticated user if successful, None otherwise
            
        Raises:
            HTTPException: If the credentials are invalid or user is not verified
        """
        user = await repository_users.get_user_by_email(db, email)
        if not user:
            return None
        
        if not self.verify_password(password, user.hashed_password):
            return None
        
        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email not verified"
            )
        
        return user

    async def register_user(self, user_data: UserCreate, db: AsyncSession) -> UserResponse:
        """
        Register a new user.
        
        Args:
            user_data: UserCreate - The user data for registration
            db: AsyncSession - Database session
            
        Returns:
            UserResponse: The created user
            
        Raises:
            HTTPException: If email is already registered
        """
        existing_user = await repository_users.get_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        
        hashed_password = pwd_context.hash(user_data.password)
        user = await repository_users.create_user(
            db,
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            role=user_data.role or UserRole.USER
        )
        return UserResponse.from_orm(user)

    def create_tokens(self, user: User) -> TokenResponse:
        access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
        access_token = self.create_access_token(
            data={"sub": user.email, "role": user.role},
            expires_delta=access_token_expires
        )
        refresh_token = self.create_refresh_token(
            data={"sub": user.email, "role": user.role}
        )
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )

    async def update_user_role(self, db: AsyncSession, user_id: int, new_role: UserRole, current_user: User) -> User:
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        user = await repository_users.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user_update = UserUpdate(role=new_role)
        return await repository_users.update_user(db, user_id, user_update)

    async def update_user_status(self, db: AsyncSession, user_id: int, is_active: bool, current_user: User) -> User:
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        user = await repository_users.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user_update = UserUpdate(is_active=is_active)
        return await repository_users.update_user(db, user_id, user_update)

    def create_token_data(self, user: User) -> TokenData:
        return TokenData(email=user.email, role=user.role)

    async def get_current_admin_user(self, current_user: User) -> User:
        """
        Get the current user and verify they have admin role.
        
        Args:
            current_user: User - The current authenticated user
            
        Returns:
            User: The current user if they are an admin
            
        Raises:
            HTTPException: If user is not an admin
        """
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough privileges"
            )
        return current_user

    async def verify_user_email(self, email: str, db: AsyncSession) -> Optional[UserResponse]:
        user = await repository_users.get_user_by_email(db, email)
        if not user:
            return None
        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already verified"
            )
        await repository_users.confirmed_email(db, email)
        return UserResponse.from_orm(user)

    async def get_current_active_user(self, current_user: User = Depends(get_current_user)) -> User:
        if not current_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        return current_user

    async def verify_verification_token(self, token: str) -> Optional[str]:
        """
        Verify a JWT verification token and return the email if valid.
        
        Args:
            token: str - The token to verify
            
        Returns:
            Optional[str]: The email from the token if valid, None otherwise
            
        Raises:
            HTTPException: If the token is invalid or expired
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload.get("type") != "verification":
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Invalid token type"
                )
            email: str = payload.get("sub")
            if email is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Email not found in token"
                )
            return email
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid or expired verification token"
            )

    async def verify_access_token(self, token: str) -> Optional[dict]:
        """Verify a JWT access token and return the payload if valid."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload.get("type") != "access":
                return None
            return payload
        except JWTError:
            return None

# Create a singleton instance
auth_service = AuthService()

# Create a dependency for getting the current user
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_db)) -> User:
    """
    Get the current authenticated user.
    
    Args:
        token: str - The JWT token from the request
        db: AsyncSession - The database session
        
    Returns:
        User: The authenticated user
        
    Raises:
        HTTPException: If the token is invalid or user not found
    """
    return await auth_service.get_current_user(token, db)

# Create a dependency for getting the current admin user
async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get the current user and verify they have admin role.
    
    Args:
        current_user: User - The current authenticated user
        
    Returns:
        User: The current user if they are an admin
        
    Raises:
        HTTPException: If user is not an admin
    """
    return await auth_service.get_current_admin_user(current_user)
