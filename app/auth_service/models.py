﻿from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.database import BaseWithId


class User(BaseWithId):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    posts = relationship(
        "Post",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    comments = relationship(
        "Comment",
        back_populates="author",
        cascade="all, delete-orphan"
    )