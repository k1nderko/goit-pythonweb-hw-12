from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import SessionLocal


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async database sessions.
    
    Yields:
        AsyncSession: An async database session.
    """
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close() 