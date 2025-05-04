from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.comment.schemas import Comment, CommentCreate
from app.db.database import get_async_session
from app.auth.security import get_current_auth_user
from app.auth.models import User

from .services import (
    fetch_comments_by_post_id,
    add_comment_for_post,
    update_user_comment,
    remove_comment_by_user
)

router = APIRouter(
    prefix="/comments",
    tags=["Comments"],
    dependencies=[Depends(HTTPBearer(auto_error=False))]
)

@router.get("/post/{post_id}", response_model=list[Comment])
async def get_comments_for_post(post_id: int, session: AsyncSession = Depends(get_async_session)):
    return await fetch_comments_by_post_id(post_id, session)

@router.post("/post/{post_id}", response_model=Comment)
async def create_comment_for_post(
    post_id: int,
    comment_data: CommentCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_auth_user)
):

    return await add_comment_for_post(post_id, comment_data, session, current_user.id)


@router.put("/{comment_id}", response_model=Comment)
async def update_comment(
    comment_id: int,
    comment_data: CommentCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_auth_user)
):
    return await update_user_comment(comment_id, comment_data, session, current_user.id)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_auth_user)
):
    await remove_comment_by_user(comment_id, session, current_user.id)


