from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from src.conf.config import DATABASE_URL
from src.schemas import UserCreate
from passlib.context import CryptContext

SECRET_KEY = DATABASE_URL
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
        Hash a password using bcrypt algorithm.

        Args:
            password (str): The plain text password to be hashed.

        Returns:
            str: The hashed password.
        """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
        Verify if a plain password matches the hashed password.

        Args:
            plain_password (str): The plain text password to verify.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
        Create a new access token with a specified expiration time.

        Args:
            data (dict): The data to encode into the token (usually user information).
            expires_delta (timedelta | None): The time delta to define the token expiration.
            If not provided, defaults to 30 minutes.

        Returns:
            str: The encoded JWT token.
        """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> str:
    """
       Verify the validity of a JWT token and extract the user's email.

       Args:
           token (str): The JWT token to verify.

       Returns:
           str: The user's email if the token is valid.

       Raises:
           JWTError: If the token is invalid or expired.
       """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise JWTError
        return email
    except JWTError:
        raise JWTError("Could not validate credentials")
