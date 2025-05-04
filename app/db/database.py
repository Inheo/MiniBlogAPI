from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import  async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from app.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            yield session

class Base(DeclarativeBase):
    __abstract__ = True

class BaseWithId(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
