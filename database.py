import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from dotenv import load_dotenv

# Load .env file into os.environ so os.getenv() can read it
load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', 
        env_file_encoding='utf-8',
        extra='ignore'  # Ignore extra fields in .env that aren't defined in the class
    )

    database_url: str = os.getenv('DATABASE_URL', 'postgresql+asyncpg://postgres:postgres@mage-postgres:5432/indian_sm_dw')
    port: int = int(os.getenv('PORT', '8000'))

settings = Settings()

DATABASE_URL = settings.database_url

# Only print in development mode
if os.getenv('DEBUG', 'true').lower() == 'true':
    print(f"Database URL: {DATABASE_URL}")
    print(f"Port: {settings.port}")

# Configure engine with production-ready settings
engine = create_async_engine(
    DATABASE_URL, 
    echo=os.getenv('DEBUG', 'true').lower() == 'true',  # Only echo in debug mode
    future=True,
    pool_size=5,  # Connection pool size
    max_overflow=10,  # Max overflow connections
    pool_pre_ping=True,  # Validate connections before use
    pool_recycle=3600  # Recycle connections every hour
)

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