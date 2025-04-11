import asyncio
import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from sqlalchemy.ext.asyncio import create_async_engine
from src.database.models import Base

# Set test database URL
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

# Create engine for test database
engine = create_async_engine(
    "sqlite:///./test.db",
    echo=True
)

async def init_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_test_db()) 