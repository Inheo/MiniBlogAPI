from fastapi import FastAPI
from app.routers import posts

app = FastAPI(title="Mini Blog API")

app.include_router(posts.router, prefix="/posts", tags=["Posts"])