"""enforce numeric remna id and drop legacy user_remna_id (UUID)

Completes the switch to numeric Remnawave user identity. Migration 0041 added
`user_remna_num_id` and backfilled it from the panel. This migration makes that
column NOT NULL and drops the legacy `user_remna_id` (UUID) column together with
its index.

Prerequisite: every `subscriptions.user_remna_num_id` must be populated. If 0041
left rows NULL (panel unreachable / user missing at backfill time), the NOT NULL
alter below will fail. Re-run the backfill first:
`alembic downgrade 0041 && alembic upgrade head` (with the panel reachable).
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0042"
down_revision: Union[str, None] = "0041"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "subscriptions",
        "user_remna_num_id",
        existing_type=sa.BigInteger(),
        nullable=False,
    )
    op.drop_index("ix_subscriptions_user_remna_id", table_name="subscriptions")
    op.drop_column("subscriptions", "user_remna_id")


def downgrade() -> None:
    op.add_column(
        "subscriptions",
        sa.Column("user_remna_id", sa.UUID(), nullable=True),
    )
    op.create_index(
        "ix_subscriptions_user_remna_id",
        "subscriptions",
        ["user_remna_id"],
        unique=False,
    )
    op.alter_column(
        "subscriptions",
        "user_remna_num_id",
        existing_type=sa.BigInteger(),
        nullable=True,
    )
