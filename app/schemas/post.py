from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    content: str

class PostResponse(PostCreate):
    id: int

    class Config:
        orm_mode = True