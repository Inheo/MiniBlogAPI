from pydantic import BaseModel

class CommentBase(BaseModel):
    __abstract__= True

    content: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    post_id: int
    user_id: int

    class Config:
        from_attributes = True
