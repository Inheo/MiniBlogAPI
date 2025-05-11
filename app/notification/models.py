from datetime import datetime

from sqlalchemy import ForeignKey, Integer, String, Bool
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class Notification(Base):
    __tablename__ = "notifications"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    message: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(default_factory=datetime.now)
    is_read: Mapped[bool] = mapped_column(Bool, default=False)

    user = relationship("User", back_populates="notifications")