# app/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite bazaga ulanish manzili
DATABASE_URL = "sqlite+aiosqlite:///support_tickets.db"

# Asinxron dvigatel
engine = create_async_engine(DATABASE_URL, echo=True)

# Asinxron sessiya klassi
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Bazaviy model klassi
Base = declarative_base()

# Session dependency (FastAPI uchun)
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
