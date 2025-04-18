from sqlalchemy import select
from sqlalchemy.ext.asyncio import  create_async_engine , async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine('sqlite+aiosqlite:///books.db', echo=True)

new_session = async_sessionmaker(engine,expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


class Base(DeclarativeBase):
    pass
