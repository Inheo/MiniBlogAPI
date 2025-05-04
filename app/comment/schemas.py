from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class CommentBase(BaseModel):
    content: str = Field(..., max_length=300)
    parent_id: Optional[int] = None

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    post_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
