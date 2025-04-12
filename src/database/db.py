"""
Database Configuration Module

This module provides the core database configuration for the application.
It sets up the SQLAlchemy async engine and session factory, and provides
functions for database initialization and session management.

Components:
- Async database engine
- Async session factory
- Database initialization function
- Session dependency function
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os
from typing import AsyncGenerator

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./contacts.db")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

# Create async session factory
SessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def init_db():
    """
    Initialize the database by creating all tables.
    
    This function should be called when the application starts
    to ensure all database tables exist.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting database sessions.
    
    Yields:
        AsyncSession: A database session that will be automatically closed
        when the context manager exits.
    """
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
