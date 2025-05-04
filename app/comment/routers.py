from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.comment import schemas, models
from app.db.database import get_async_session
from app.auth.security import get_current_auth_user
from app.auth import models as auth_models
from app.post.models import Post

router = APIRouter(
    prefix="/comments",
    tags=["Comments"],
    dependencies=[Depends(HTTPBearer(auto_error=False))]
)

@router.get("/post/{post_id}", response_model=list[schemas.Comment])
async def get_comments_for_post(post_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(models.Comment).where(models.Comment.post_id == post_id))
    return result.scalars().all()

@router.post("/post/{post_id}", response_model=schemas.Comment)
async def create_comment_for_post(
    post_id: int,
    comment_data: schemas.CommentCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: auth_models.User = Depends(get_current_auth_user)
):
    post = await session.get(Post, post_id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if comment_data.parent_id:
        parent = await session.get(models.Comment, comment_data.parent_id)
        if not parent or parent.post_id != post_id:
            raise HTTPException(status_code=400, detail="Invalid parent comment")


    comment = models.Comment(
        content=comment_data.content,
        post_id=post.id,
        user_id=current_user.id,
        parent_id = comment_data.parent_id
    )

    session.add(comment)
    await session.flush()
    return comment


@router.put("/{comment_id}", response_model=schemas.Comment)
async def update_comment(
    comment_id: int,
    comment_data: schemas.CommentCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: auth_models.User = Depends(get_current_auth_user)
):

    comment = get_comment_by_user(comment_id, session, current_user)

    comment.content = comment_data.content
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    session: AsyncSession = Depends(get_async_session),
   current_user: auth_models.User = Depends(get_current_auth_user)
):
    comment = get_comment_by_user(comment_id, session, current_user)

    await session.delete(comment)


async def get_comment_by_user(comment_id:int, session: AsyncSession, current_user: auth_models.User) -> models.Comment:
    comment: models.Comment | None = await session.get(models.Comment, comment_id)

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    if not comment.user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your comment")

    return comment