from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database.models import User
from src.schemas import UserCreate
from src.utils.password import get_password_hash


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    """
    Create a new user.
    
    Args:
        db: AsyncSession - The database session
        user: UserCreate - The user data to create
        
    Returns:
        User: The created user
    """
    db_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """
    Get a user by email.
    
    Args:
        db: AsyncSession - The database session
        email: str - The email to search for
        
    Returns:
        User | None: The user if found, None otherwise
    """
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()


async def verify_user_email(db: AsyncSession, email: str) -> User | None:
    """
    Verify a user's email.
    
    Args:
        db: AsyncSession - The database session
        email: str - The email to verify
        
    Returns:
        User | None: The verified user if found, None otherwise
    """
    user = await get_user_by_email(db, email)
    if user:
        user.is_verified = True
        await db.commit()
        await db.refresh(user)
    return user
