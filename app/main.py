from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.auth_service import routers as auth_router
from app.post_service import routers as post_router
from app.comment_service import routers as comment_router
from app.db import database


@asynccontextmanager
async def lifespan(fast_app: FastAPI):
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)
    yield

    database.engine.dispose()

app = FastAPI(title="Mini Blog API", lifespan=lifespan)

app.include_router(auth_router.router)
app.include_router(post_router.router)
app.include_router(comment_router.router)