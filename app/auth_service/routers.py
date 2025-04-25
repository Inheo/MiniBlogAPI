from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.auth_service import schemas, models
from app.db.database import get_async_session
from app.auth_service.security import (
    hash_password,
    verify_password,
    generate_token,
    get_current_auth_user_for_refresh,
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    dependencies=[Depends(HTTPBearer(auto_error=False))]
)

@router.post("/register", response_model=schemas.Token)
async def register_user(user_data: schemas.UserCreate, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(models.User).where(models.User.email == user_data.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    user = models.User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return generate_token(user)


@router.post("/token", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(models.User).where(models.User.email == form_data.username))
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    return generate_token(user)


@router.post("/refresh", response_model=schemas.Token)
def refresh_token(
    current_user: models.User = Depends(get_current_auth_user_for_refresh)
):
    return generate_token(current_user)