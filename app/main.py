from fastapi import FastAPI
from app.routers import posts
from app.db.database import Base, engine
from app.db import models

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Mini Blog API")

app.include_router(posts.router, prefix="/posts", tags=["Posts"])