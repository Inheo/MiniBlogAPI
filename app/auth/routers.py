from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from .schemas import UserCreate, Token
from .models import User
from .services import (
    register_new_user,
    login_new
)
from .security import (
    get_current_auth_user_for_refresh,
    generate_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    dependencies=[Depends(HTTPBearer(auto_error=False))]
)

@router.post("/register", response_model=Token)
async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    return await register_new_user(user_data, session)


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    user_data = UserCreate(email=form_data.username, password=form_data.password)
    return await login_new(user_data, session)


@router.post("/refresh", response_model=Token)
def refresh_token(
    current_user: User = Depends(get_current_auth_user_for_refresh)
):
    return generate_token(current_user)