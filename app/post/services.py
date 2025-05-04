from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.post.schemas import PostCreate
from .models import Post


async def fetch_all_posts(session: AsyncSession):
    result = await session.execute(select(Post))
    return result.scalars().all()


async def fetch_post_by_id(post_id: int, session: AsyncSession):
    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


async def add_post(
    post_data: PostCreate,
    session: AsyncSession,
    current_user_id: int
):
    new_post = Post(**post_data.model_dump(), owner_id=current_user_id)
    session.add(new_post)
    await session.flush()
    return new_post


async def update_user_post(
    post_id: int,
    post_data: PostCreate,
    session: AsyncSession,
    current_user_id: int
):
    post = await fetch_post_by_id(post_id, session)

    if post.owner_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")

    post.title = post_data.title
    post.content = post_data.content
    return post


async def remove_post(
    post_id: int,
    session: AsyncSession,
    current_user_id: int
):
    post = await fetch_post_by_id(post_id, session)

    if post.owner_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")

    await session.delete(post)