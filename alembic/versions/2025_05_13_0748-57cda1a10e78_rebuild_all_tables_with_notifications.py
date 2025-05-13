"""rebuild all tables with notifications

Revision ID: 57cda1a10e78
Revises: 3fdb8df82a91
Create Date: 2025-05-13 07:48:02.784970

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "57cda1a10e78"
down_revision: Union[str, None] = "3fdb8df82a91"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "notifications",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("message", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("is_read", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_index("ix_comments_id", table_name="comments")
    op.drop_index("ix_posts_id", table_name="posts")
    op.drop_index("ix_users_id", table_name="users")


def downgrade() -> None:
    """Downgrade schema."""
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index("ix_posts_id", "posts", ["id"], unique=False)
    op.create_index("ix_comments_id", "comments", ["id"], unique=False)
    op.drop_table("notifications")
