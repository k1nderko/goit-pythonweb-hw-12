from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.config import settings
from src.database.session import get_async_db
from src.repository import users as repository_users
from src.utils.password import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

class Auth:
    """
    Authentication service for handling JWT tokens.
    """
    secret_key = settings.SECRET_KEY
    algorithm = settings.ALGORITHM
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against a hashed password.
        
        Args:
            plain_password: str - The plain text password
            hashed_password: str - The hashed password to compare against
            
        Returns:
            bool: True if the passwords match, False otherwise
        """
        return verify_password(plain_password, hashed_password)
    
    def create_access_token(self, data: dict) -> str:
        """
        Create an access token.
        
        Args:
            data: dict - The data to encode in the token
            
        Returns:
            str: The encoded JWT token
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
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
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return token
    
    def create_verification_token(self, email: str) -> str:
        """
        Create an email verification token.
        
        Args:
            email: str - The email to encode in the token
            
        Returns:
            str: The encoded JWT token
        """
        to_encode = {"sub": email}
        expire = datetime.utcnow() + timedelta(hours=24)
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return token
    
    def verify_token(self, token: str) -> Optional[str]:
        """
        Verify a JWT token.
        
        Args:
            token: str - The token to verify
            
        Returns:
            Optional[str]: The email from the token if valid, None otherwise
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            email: str = payload.get("sub")
            if email is None:
                return None
            return email
        except JWTError:
            return None

    def decode_token(self, token: str) -> dict:
        """
        Decode a JWT token.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None

    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_db)):
        """
        Get the current authenticated user.
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

# Create a singleton instance
auth_service = Auth()

# Create a dependency for getting the current user
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_db)):
    return await auth_service.get_current_user(token, db)
