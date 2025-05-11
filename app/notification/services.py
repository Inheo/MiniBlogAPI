from typing import List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import NotificationCreate
from .models import Notification


async def create_notification(notification_data: NotificationCreate, session: AsyncSession) -> Notification:
    notification = Notification(**notification_data.model_dump())
    session.add(notification)
    await session.flush()
    return notification


async def get_notifications(user_id: int, session: AsyncSession) -> List[Notification]:
    result = await session.execute(
        select(Notification)
        .where(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
    )

    return result.scalars().all()


async def mark_all_notifications_read(user_id: int, session: AsyncSession) -> None:
    await session.execute(
        update(Notification)
        .where(Notification.user_id == user_id, Notification.is_read == False)
        .values(is_read=True)
    )