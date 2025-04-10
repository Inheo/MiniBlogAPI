from fastapi import FastAPI
from app.auth_service import routers as auth_router
from app.post_service import routers as post_router
from app.db import database

app = FastAPI(title="Mini Blog API")
database.Base.metadata.create_all(bind=database.engine)

app.include_router(auth_router.router)
app.include_router(post_router.router)