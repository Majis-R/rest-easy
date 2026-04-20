from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.secrets import secrets

# Create the async engine
# echo=True prints SQL queries to the console for debugging
engine = create_async_engine(secrets.DATABASE_URL, echo=True)

# Create a customized session maker
async_session_maker = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# All database models will inherit from this Base
class Base(DeclarativeBase):
    pass

# Dependency to get a database session per request
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session