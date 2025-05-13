from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.auth import routers as auth_router
from app.post import routers as post_router
from app.comment import routers as comment_router
from app.notification import routers as notification_router
from app.db import database
import event_listeners


@asynccontextmanager
async def lifespan(fast_app: FastAPI):
    yield

    database.engine.dispose()

app = FastAPI(title="Mini Blog API", lifespan=lifespan)

app.include_router(auth_router.router)
app.include_router(post_router.router)
app.include_router(comment_router.router)
app.include_router(notification_router.router)