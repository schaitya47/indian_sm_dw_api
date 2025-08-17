import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession # Make sure AsyncSession is imported
from typing import AsyncGenerator

class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    database_url: str = os.getenv('DATABASE_URL', 'postgresql+asyncpg://postgres:postgres@localhost:5432/indian_sm_dw')

settings = Settings()

DATABASE_URL = settings.database_url

print(DATABASE_URL)

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session for FastAPI dependencies.

    Why this is needed:
    - Provides a per-request AsyncSession that endpoints can depend on with Depends(get_db).
    - Ensures proper lifecycle: session is opened, yielded to the path operation, then committed on success
      or rolled back on exception, and always closed to avoid connection leaks.
    - Makes tests easier because the dependency can be overridden.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise