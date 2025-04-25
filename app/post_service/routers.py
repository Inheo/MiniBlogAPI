from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.database import get_async_session
from app.post_service import models, schemas
from app.auth_service import models as auth_models
from app.auth_service.security import get_current_auth_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    dependencies=[Depends(HTTPBearer(auto_error=False))]
)


@router.get("/", response_model=List[schemas.Post])
async def get_all_posts(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(models.Post))
    posts = result.scalars().all()
    return posts


@router.get("/{post_id}", response_model=schemas.Post)
async def get_post_by_id(post_id: int, session: AsyncSession = Depends(get_async_session)):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    result = await session.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: schemas.PostCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: auth_models.User = Depends(get_current_auth_user),
):
    new_post = models.Post(**post_data.model_dump(), owner_id=current_user.id)
    print(new_post)
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)
    return new_post


@router.put("/{post_id}", response_model=schemas.Post)
async def update_post(
    post_id: int,
    post_data: schemas.PostCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: auth_models.User = Depends(get_current_auth_user),
):
    result = await session.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")

    post.title = post_data.title
    post.content = post_data.content
    await session.commit()
    await session.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: auth_models.User = Depends(get_current_auth_user),
):
    result = await session.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")

    await session.delete(post)
    await session.commit()
