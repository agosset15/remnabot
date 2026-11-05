"""birthday greetings: cache the user's Telegram birthdate and the last gift year

`users.birth_day` / `users.birth_month` hold the birthdate from Telegram `getChat`
(NULL when hidden or not set), `users.birthdate_synced_at` is when it was last fetched,
and `users.birthday_gift_year` is the year the last birthday gift was granted.
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0044"
down_revision: Union[str, None] = "0043"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("birth_day", sa.SmallInteger(), nullable=True))
    op.add_column("users", sa.Column("birth_month", sa.SmallInteger(), nullable=True))
    op.add_column(
        "users", sa.Column("birthdate_synced_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column("users", sa.Column("birthday_gift_year", sa.Integer(), nullable=True))
    op.create_index("ix_users_birth_month_day", "users", ["birth_month", "birth_day"])


def downgrade() -> None:
    op.drop_index("ix_users_birth_month_day", table_name="users")
    op.drop_column("users", "birthday_gift_year")
    op.drop_column("users", "birthdate_synced_at")
    op.drop_column("users", "birth_month")
    op.drop_column("users", "birth_day")
