from sqlalchemy.ext.asyncio import AsyncSession

from app.core.events import emit
from app.core.event_types import EventType
from app.post.models import Post
from app.comment.models import Comment
from app.core.event_payloads import CommentCreated


async def user_commented_on_post_or_comment(post: Post, comment: Comment, session: AsyncSession):
    payload = CommentCreated(
        comment_id=comment.id,
        post_id=post.id,
        post_title=post.title,
        post_owner_id=post.owner_id,
        author_id=comment.user_id
    )

    await emit(EventType.USER_COMMENTED_ON_POST_OR_COMMENT, payload, session)

