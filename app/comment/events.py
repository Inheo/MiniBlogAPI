from sqlalchemy.ext.asyncio import AsyncSession

from app.core.events import emit
from app.core.event_types import EventType
from app.post.models import Post
from app.comment.models import Comment
from app.core.event_payloads import CommentCreated


async def user_commented_on_post_or_comment(post: Post, comment: Comment, session: AsyncSession):
    payload = CommentCreated(
        author_comment_id=comment.user_id,
        comment_id=comment.id,
        comment_parent_id=comment.parent_id,
        comment_content=comment.content,
        post_id=post.id,
        post_owner_id=post.owner_id
    )

    await emit(EventType.USER_COMMENTED_ON_POST_OR_COMMENT, payload, session)

