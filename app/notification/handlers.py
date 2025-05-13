from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.events import on
from app.core.event_payloads import CommentCreated
from app.core.event_types import EventType
from app.comment.models import Comment
from .schemas import NotificationCreate
from .services import create_notification


@on(EventType.USER_COMMENTED_ON_POST_OR_COMMENT)
async def handle_comment_created_notification(payload: CommentCreated, session: AsyncSession):
    await try_create_notification_for_parent_comment_owner(payload, session)
    await try_create_notification_for_post_owner(payload, session)


async def try_create_notification_for_parent_comment_owner(payload: CommentCreated, session: AsyncSession):
    if payload.comment_parent_id is not None and payload.comment_parent_id != 0:
        result = await session.execute(select(Comment.user_id).where(Comment.id == payload.comment_parent_id))
        parent_comment_owner_id = result.scalar_one_or_none()

        if parent_comment_owner_id:
            if parent_comment_owner_id != payload.author_comment_id:
                await create_notification_for_parent_comment_owner(parent_comment_owner_id, payload, session)


async def create_notification_for_parent_comment_owner(
        parent_comment_owner_id: int,
        payload: CommentCreated,
        session: AsyncSession
):
    notification = NotificationCreate(
        user_id=parent_comment_owner_id,
        message=f"Replied to your comment on the post: '{payload.comment_content}'"
    )
    await create_notification(notification, session)


async def try_create_notification_for_post_owner(payload: CommentCreated, session: AsyncSession):
    if payload.author_comment_id != payload.post_owner_id:
        await create_notification_for_post_owner(payload, session)


async def create_notification_for_post_owner(payload: CommentCreated, session: AsyncSession):
    notification = NotificationCreate(
        user_id=payload.post_owner_id,
        message=f"New comment on your post: '{payload.comment_content}'"
    )
    await create_notification(notification, session)