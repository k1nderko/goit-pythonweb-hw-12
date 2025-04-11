from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database.models import User, UserRole
from src.schemas import UserCreate
from src.utils.password import get_password_hash
from typing import Optional, List


async def create_user(
    db: AsyncSession,
    email: str,
    hashed_password: str,
    full_name: Optional[str] = None,
    role: UserRole = UserRole.USER
) -> User:
    """
    Create a new user.
    
    Args:
        db: AsyncSession - Database session
        email: str - User's email
        hashed_password: str - Hashed password
        full_name: Optional[str] - User's full name
        role: UserRole - User's role (defaults to USER)
        
    Returns:
        User: The created user
    """
    existing_user = await get_user_by_email(db, email)
    if existing_user:
        raise ValueError("Email already registered")
    
    user = User(
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        role=role
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """
    Get a user by their email address.
    
    Args:
        db: AsyncSession - Database session
        email: str - The email to search for
        
    Returns:
        Optional[User]: The user if found, None otherwise
    """
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """
    Get a user by ID.
    
    Args:
        db: AsyncSession - The database session
        user_id: int - The user ID to search for
        
    Returns:
        User | None: The user if found, None otherwise
    """
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[User]:
    """
    Get all users with pagination.
    
    Args:
        db: AsyncSession - The database session
        skip: int - The number of users to skip
        limit: int - The maximum number of users to return
        
    Returns:
        list[User]: The list of users
    """
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def get_users_by_role(db: AsyncSession, role: UserRole, skip: int = 0, limit: int = 100) -> list[User]:
    """
    Get users by role with pagination.
    
    Args:
        db: AsyncSession - The database session
        role: UserRole - The role to filter by
        skip: int - The number of users to skip
        limit: int - The maximum number of users to return
        
    Returns:
        list[User]: The list of users
    """
    result = await db.execute(
        select(User)
        .where(User.role == role)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def update_user_role(db: AsyncSession, user_id: int, role: UserRole) -> User | None:
    """
    Update a user's role.
    
    Args:
        db: AsyncSession - The database session
        user_id: int - The user ID to update
        role: UserRole - The new role
        
    Returns:
        User | None: The updated user if found, None otherwise
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    
    user.role = role
    await db.commit()
    await db.refresh(user)
    return user


async def update_user_active_status(db: AsyncSession, user_id: int, is_active: bool) -> User | None:
    """
    Update a user's active status.
    
    Args:
        db: AsyncSession - The database session
        user_id: int - The user ID to update
        is_active: bool - The new active status
        
    Returns:
        User | None: The updated user if found, None otherwise
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    
    user.is_active = is_active
    await db.commit()
    await db.refresh(user)
    return user


async def update_user_verified_status(db: AsyncSession, user_id: int, is_verified: bool) -> User | None:
    """
    Update a user's verified status.
    
    Args:
        db: AsyncSession - The database session
        user_id: int - The user ID to update
        is_verified: bool - The new verified status
        
    Returns:
        User | None: The updated user if found, None otherwise
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    
    user.is_verified = is_verified
    await db.commit()
    await db.refresh(user)
    return user


async def update_user_password(db: AsyncSession, user_id: int, hashed_password: str) -> User | None:
    """
    Update a user's password.
    
    Args:
        db: AsyncSession - The database session
        user_id: int - The user ID to update
        hashed_password: str - The new hashed password
        
    Returns:
        User | None: The updated user if found, None otherwise
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    
    user.hashed_password = hashed_password
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    """
    Delete a user.
    
    Args:
        db: AsyncSession - The database session
        user_id: int - The user ID to delete
        
    Returns:
        bool: True if the user was deleted, False otherwise
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        return False
    
    await db.delete(user)
    await db.commit()
    return True


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


async def update_user(db: AsyncSession, user: User, **kwargs) -> User:
    """
    Update a user's attributes.
    
    Args:
        db: AsyncSession - Database session
        user: User - The user to update
        **kwargs: Additional fields to update
        
    Returns:
        User: The updated user
    """
    for key, value in kwargs.items():
        if hasattr(user, key) and value is not None:
            setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return user


async def update_token(db: AsyncSession, user: User, token: Optional[str] = None) -> None:
    """
    Update a user's refresh token.
    
    Args:
        db: AsyncSession - Database session
        user: User - The user to update
        token: Optional[str] - The new refresh token
    """
    user.refresh_token = token
    await db.commit()


async def confirmed_email(db: AsyncSession, email: str) -> None:
    """
    Mark a user's email as verified.
    
    Args:
        db: AsyncSession - Database session
        email: str - The email to verify
    """
    user = await get_user_by_email(db, email)
    user.is_verified = True
    await db.commit()


async def update_user_verified(db: AsyncSession, user_id: int, is_verified: bool) -> Optional[User]:
    """
    Update user's verification status.
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    
    user.is_verified = is_verified
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
