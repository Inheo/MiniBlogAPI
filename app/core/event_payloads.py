from typing import Optional

from pydantic import BaseModel


class EventBase(BaseModel):
    pass

class CommentCreated(EventBase):
    author_comment_id: int
    comment_id: int
    comment_parent_id: Optional[int] = None
    comment_content: str
    post_id: int
    post_owner_id: int
