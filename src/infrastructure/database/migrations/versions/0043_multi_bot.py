"""multi-bot support: remember each user's bot and the bot of broadcast messages

`users.bot_id` stores the Telegram bot the user last interacted with, so outgoing
messages go through a bot the user has started. NULL means the primary bot.

`broadcast_messages.bot_id` stores the bot that delivered a broadcast message, so it
can be deleted through the same bot later. NULL means the primary bot.
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0043"
down_revision: Union[str, None] = "0042"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("bot_id", sa.BigInteger(), nullable=True))
    op.add_column("broadcast_messages", sa.Column("bot_id", sa.BigInteger(), nullable=True))


def downgrade() -> None:
    op.drop_column("broadcast_messages", "bot_id")
    op.drop_column("users", "bot_id")
