from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.auth.security import get_current_auth_user
from app.db.database import get_async_session
from app.notification.schemas import Notification

from .services import (
    get_notifications,
    mark_all_notifications_read
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
    dependencies=[Depends(HTTPBearer(auto_error=False))]
)

@router.get("/", response_model=List[Notification])
async def get_all_notifications_for_user(
        user: User = Depends(get_current_auth_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await get_notifications(user.id, session)

@router.patch("/mark-all-read", status_code=status.HTTP_204_NO_CONTENT)
async def mark_all_read(
        user: User = Depends(get_current_auth_user),
        session: AsyncSession = Depends(get_async_session)
):
    await mark_all_notifications_read(user.id, session)