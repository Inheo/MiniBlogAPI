from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.post.models import Post
from .schemas import CommentCreate
from .models import Comment


async def fetch_comments_by_post_id(post_id: int, session: AsyncSession) -> [Comment]:
    result = await session.execute(select(Comment).where(Comment.post_id == post_id))
    return result.scalars().all()


async def add_comment_for_post(
    post_id: int,
    comment_data: CommentCreate,
    session: AsyncSession,
    current_user_id: int
) -> Comment:
    post = await session.get(Post, post_id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if comment_data.parent_id:
        parent = await session.get(Comment, comment_data.parent_id)
        if not parent or parent.post_id != post_id:
            raise HTTPException(status_code=400, detail="Invalid parent comment")


    comment = Comment(
        content=comment_data.content,
        post_id=post.id,
        user_id=current_user_id,
        parent_id = comment_data.parent_id
    )

    session.add(comment)
    await session.flush()
    return comment


async def update_user_comment(
    comment_id: int,
    comment_data: CommentCreate,
    session: AsyncSession,
    current_user_id: int
) -> Comment:
    comment = await get_comment_by_user(comment_id, session, current_user_id)
    comment.content = comment_data.content
    return comment


async def remove_comment_by_user(
    comment_id: int,
    session: AsyncSession,
    current_user_id: int
):
    comment = await get_comment_by_user(comment_id, session, current_user_id)
    await session.delete(comment)


async def get_comment_by_user(comment_id:int, session: AsyncSession, current_user_id: int) -> Comment:
    comment: Comment | None = await session.get(Comment, comment_id)

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    if not comment.user_id == current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your comment")

    return comment