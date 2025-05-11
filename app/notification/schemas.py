from datetime import datetime

from pydantic import BaseModel

class NotificationCreate(BaseModel):
    user_id: int
    message: str

class Notification(NotificationCreate):
    id: int
    created_at: datetime
    is_read: bool