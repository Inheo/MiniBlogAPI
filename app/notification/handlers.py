from sqlalchemy.ext.asyncio import AsyncSession

from app.core.events import on
from app.core.event_payloads import CommentCreated
from app.core.event_types import EventType
from .schemas import NotificationCreate
from .services import create_notification


@on(EventType.USER_COMMENTED_ON_POST_OR_COMMENT)
async def notify_post_owner(payload: CommentCreated, session: AsyncSession):
    if payload.author_id != payload.post_owner_id:
        notification = NotificationCreate(
            user_id=payload.post_owner_id,
            message=f"New comment on your post: '{payload.post_title}'"
        )
        await create_notification(notification, session)