from pydantic import BaseModel


class EventBase(BaseModel):
    pass

class CommentCreated(EventBase):
    comment_id: int
    post_id: int
    post_title: str
    post_owner_id: int
    author_id: int
