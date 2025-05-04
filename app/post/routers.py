from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_async_session
from app.post.schemas import Post, PostCreate
from app.auth import models as auth_models
from app.auth.security import get_current_auth_user
from .services import (
    fetch_all_posts,
    fetch_post_by_id,
    add_post,
    update_user_post,
    remove_post
)

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    dependencies=[Depends(HTTPBearer(auto_error=False))]
)


@router.get("/", response_model=List[Post])
async def get_all_posts(session: AsyncSession = Depends(get_async_session)):
    return await fetch_all_posts(session)


@router.get("/{post_id}", response_model=Post)
async def get_post_by_id(post_id: int, session: AsyncSession = Depends(get_async_session)):
    return await fetch_post_by_id(post_id, session)


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: auth_models.User = Depends(get_current_auth_user),
):
    return await add_post(post_data, session, current_user.id)


@router.put("/{post_id}", response_model=Post)
async def update_post(
    post_id: int,
    post_data: PostCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: auth_models.User = Depends(get_current_auth_user),
):
    return update_user_post(post_id, post_data, session, current_user.id)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: auth_models.User = Depends(get_current_auth_user),
):
    return await remove_post(post_id, session, current_user.id)
