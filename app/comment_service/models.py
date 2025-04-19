from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import BaseWithId

class Comment(BaseWithId):
    __tablename__ = "comments"

    content: Mapped[str] = mapped_column(String, nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")