from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .schemas import PostCreate
from .models import Post
from .exceptions import (
    PostNotFoundException,
    NotAuthorizedForUpdatePostException,
    NotAuthorizedForDeletePostException
)


async def fetch_all_posts(session: AsyncSession) -> Sequence[Post]:
    result = await session.execute(select(Post))
    return result.scalars().all()


async def fetch_post_by_id(post_id: int, session: AsyncSession) -> Post:
    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise PostNotFoundException()
    return post


async def add_post(
    post_data: PostCreate,
    session: AsyncSession,
    current_user_id: int
) -> Post:
    new_post = Post(**post_data.model_dump(), owner_id=current_user_id)
    session.add(new_post)
    await session.flush()
    return new_post


async def update_user_post(
    post_id: int,
    post_data: PostCreate,
    session: AsyncSession,
    current_user_id: int
) -> Post:
    post = await fetch_post_by_id(post_id, session)

    if post.owner_id != current_user_id:
        raise NotAuthorizedForUpdatePostException()

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
        raise NotAuthorizedForDeletePostException()

    await session.delete(post)