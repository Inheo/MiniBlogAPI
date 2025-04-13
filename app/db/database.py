#DEFAULT_DATABASE_URL = "sqlite:///./blog.db"
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from app.config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Base(DeclarativeBase):
    __abstract__ = True

class BaseWithId(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
