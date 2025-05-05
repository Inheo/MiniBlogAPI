from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .exceptions import UserAlreadyExistsException, InvalidUserCredentialsException
from .schemas import UserCreate, Token
from .models import User
from .security import (
    hash_password,
    generate_token,
    verify_password
)


async def get_user_by_email(email: EmailStr, session: AsyncSession) -> User:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def register_new_user(user_data: UserCreate, session: AsyncSession) -> Token:
    existing_user = await get_user_by_email(user_data.email, session)
    if existing_user:
        raise UserAlreadyExistsException()

    user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )

    session.add(user)
    await session.flush()
    return generate_token(user)


async def login_new(user_data: UserCreate, session: AsyncSession) -> Token:
    user = await get_user_by_email(user_data.email, session)

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise InvalidUserCredentialsException()
    return generate_token(user)