from pydantic import BaseModel, Field

class Post(BaseModel):
    id: int
    title: str = Field(..., min_length=3, max_length=100)
    content: str