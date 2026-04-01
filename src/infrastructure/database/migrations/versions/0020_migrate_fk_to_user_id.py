"""Migrate all FKs from users.telegram_id to users.id;
add email to users; make telegram_id optional; add check constraint.
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0020"
down_revision: Union[str, None] = "0019"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── 1. users: add email, make telegram_id nullable, add check constraint ──

    op.add_column("users", sa.Column("email", sa.String(255), nullable=True))
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.alter_column("users", "telegram_id", nullable=True)

    op.create_check_constraint(
        "ck_users_telegram_or_email",
        "users",
        "telegram_id IS NOT NULL OR email IS NOT NULL",
    )

    # ── 2. subscriptions: drop old FK, add user_id column, backfill, drop old column ──

    op.drop_constraint("subscriptions_user_telegram_id_fkey", "subscriptions", type_="foreignkey")
    op.drop_index("ix_subscriptions_user_telegram_id", "subscriptions")

    op.add_column("subscriptions", sa.Column("user_id", sa.Integer(), nullable=True))

    op.execute(sa.text("""
        UPDATE subscriptions s
        SET user_id = u.id
        FROM users u
        WHERE u.telegram_id = s.user_telegram_id
    """))

    op.alter_column("subscriptions", "user_id", nullable=False)
    op.create_index("ix_subscriptions_user_id", "subscriptions", ["user_id"])
    op.create_foreign_key(
        "subscriptions_user_id_fkey",
        "subscriptions",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.drop_column("subscriptions", "user_telegram_id")

    # ── 3. transactions: drop old FK, add user_id column, backfill, drop old column ──

    op.drop_constraint("transactions_user_telegram_id_fkey", "transactions", type_="foreignkey")
    op.drop_index("ix_transactions_user_telegram_id", "transactions")

    op.add_column("transactions", sa.Column("user_id", sa.Integer(), nullable=True))

    op.execute(sa.text("""
        UPDATE transactions t
        SET user_id = u.id
        FROM users u
        WHERE u.telegram_id = t.user_telegram_id
    """))

    op.alter_column("transactions", "user_id", nullable=False)
    op.create_index("ix_transactions_user_id", "transactions", ["user_id"])
    op.create_foreign_key(
        "transactions_user_id_fkey",
        "transactions",
        "users",
        ["user_id"],
        ["id"],
    )

    op.drop_column("transactions", "user_telegram_id")

    # ── 4. referrals: drop old FKs, add user_id columns, backfill, drop old columns ──

    op.drop_constraint("referrals_referrer_telegram_id_fkey", "referrals", type_="foreignkey")
    op.drop_constraint("referrals_referred_telegram_id_fkey", "referrals", type_="foreignkey")
    op.drop_index("ix_referrals_referrer_telegram_id", "referrals")
    op.drop_index("ix_referrals_referred_telegram_id", "referrals")
    op.drop_constraint("referrals_referred_telegram_id_key", "referrals", type_="unique")

    op.add_column("referrals", sa.Column("referrer_user_id", sa.Integer(), nullable=True))
    op.add_column("referrals", sa.Column("referred_user_id", sa.Integer(), nullable=True))

    op.execute(sa.text("""
        UPDATE referrals r
        SET
            referrer_user_id = u1.id,
            referred_user_id = u2.id
        FROM users u1, users u2
        WHERE u1.telegram_id = r.referrer_telegram_id
          AND u2.telegram_id = r.referred_telegram_id
    """))

    op.alter_column("referrals", "referrer_user_id", nullable=False)
    op.alter_column("referrals", "referred_user_id", nullable=False)

    op.create_index("ix_referrals_referrer_user_id", "referrals", ["referrer_user_id"])
    op.create_index("ix_referrals_referred_user_id", "referrals", ["referred_user_id"])
    op.create_unique_constraint("referrals_referred_user_id_key", "referrals", ["referred_user_id"])

    op.create_foreign_key(
        "referrals_referrer_user_id_fkey",
        "referrals",
        "users",
        ["referrer_user_id"],
        ["id"],
    )
    op.create_foreign_key(
        "referrals_referred_user_id_fkey",
        "referrals",
        "users",
        ["referred_user_id"],
        ["id"],
    )

    op.drop_column("referrals", "referrer_telegram_id")
    op.drop_column("referrals", "referred_telegram_id")

    # ── 5. referral_rewards: drop old FK, add user_id, backfill, drop old column ──

    op.drop_constraint("referral_rewards_user_telegram_id_fkey", "referral_rewards", type_="foreignkey")
    op.drop_index("ix_referral_rewards_user_telegram_id", "referral_rewards")

    op.add_column("referral_rewards", sa.Column("user_id", sa.Integer(), nullable=True))

    op.execute(sa.text("""
        UPDATE referral_rewards rr
        SET user_id = u.id
        FROM users u
        WHERE u.telegram_id = rr.user_telegram_id
    """))

    op.alter_column("referral_rewards", "user_id", nullable=False)
    op.create_index("ix_referral_rewards_user_id", "referral_rewards", ["user_id"])
    op.create_foreign_key(
        "referral_rewards_user_id_fkey",
        "referral_rewards",
        "users",
        ["user_id"],
        ["id"],
    )

    op.drop_column("referral_rewards", "user_telegram_id")


def downgrade() -> None:
    # ── referral_rewards ──
    op.drop_constraint("referral_rewards_user_id_fkey", "referral_rewards", type_="foreignkey")
    op.drop_index("ix_referral_rewards_user_id", "referral_rewards")

    op.add_column("referral_rewards", sa.Column("user_telegram_id", sa.BigInteger(), nullable=True))

    op.execute(sa.text("""
        UPDATE referral_rewards rr
        SET user_telegram_id = u.telegram_id
        FROM users u
        WHERE u.id = rr.user_id
    """))

    op.alter_column("referral_rewards", "user_telegram_id", nullable=False)
    op.create_index("ix_referral_rewards_user_telegram_id", "referral_rewards", ["user_telegram_id"])
    op.create_foreign_key(
        "referral_rewards_user_telegram_id_fkey",
        "referral_rewards",
        "users",
        ["user_telegram_id"],
        ["telegram_id"],
    )
    op.drop_column("referral_rewards", "user_id")

    # ── referrals ──
    op.drop_constraint("referrals_referrer_user_id_fkey", "referrals", type_="foreignkey")
    op.drop_constraint("referrals_referred_user_id_fkey", "referrals", type_="foreignkey")
    op.drop_constraint("referrals_referred_user_id_key", "referrals", type_="unique")
    op.drop_index("ix_referrals_referrer_user_id", "referrals")
    op.drop_index("ix_referrals_referred_user_id", "referrals")

    op.add_column("referrals", sa.Column("referrer_telegram_id", sa.BigInteger(), nullable=True))
    op.add_column("referrals", sa.Column("referred_telegram_id", sa.BigInteger(), nullable=True))

    op.execute(sa.text("""
        UPDATE referrals r
        SET
            referrer_telegram_id = u1.telegram_id,
            referred_telegram_id = u2.telegram_id
        FROM users u1, users u2
        WHERE u1.id = r.referrer_user_id
          AND u2.id = r.referred_user_id
    """))

    op.alter_column("referrals", "referrer_telegram_id", nullable=False)
    op.alter_column("referrals", "referred_telegram_id", nullable=False)

    op.create_index("ix_referrals_referrer_telegram_id", "referrals", ["referrer_telegram_id"])
    op.create_index("ix_referrals_referred_telegram_id", "referrals", ["referred_telegram_id"])
    op.create_unique_constraint("referrals_referred_telegram_id_key", "referrals", ["referred_telegram_id"])
    op.create_foreign_key(
        "referrals_referrer_telegram_id_fkey",
        "referrals",
        "users",
        ["referrer_telegram_id"],
        ["telegram_id"],
    )
    op.create_foreign_key(
        "referrals_referred_telegram_id_fkey",
        "referrals",
        "users",
        ["referred_telegram_id"],
        ["telegram_id"],
    )

    op.drop_column("referrals", "referrer_user_id")
    op.drop_column("referrals", "referred_user_id")

    # ── transactions ──
    op.drop_constraint("transactions_user_id_fkey", "transactions", type_="foreignkey")
    op.drop_index("ix_transactions_user_id", "transactions")

    op.add_column("transactions", sa.Column("user_telegram_id", sa.BigInteger(), nullable=True))

    op.execute(sa.text("""
        UPDATE transactions t
        SET user_telegram_id = u.telegram_id
        FROM users u
        WHERE u.id = t.user_id
    """))

    op.alter_column("transactions", "user_telegram_id", nullable=False)
    op.create_index("ix_transactions_user_telegram_id", "transactions", ["user_telegram_id"])
    op.create_foreign_key(
        "transactions_user_telegram_id_fkey",
        "transactions",
        "users",
        ["user_telegram_id"],
        ["telegram_id"],
    )
    op.drop_column("transactions", "user_id")

    # ── subscriptions ──
    op.drop_constraint("subscriptions_user_id_fkey", "subscriptions", type_="foreignkey")
    op.drop_index("ix_subscriptions_user_id", "subscriptions")

    op.add_column("subscriptions", sa.Column("user_telegram_id", sa.BigInteger(), nullable=True))

    op.execute(sa.text("""
        UPDATE subscriptions s
        SET user_telegram_id = u.telegram_id
        FROM users u
        WHERE u.id = s.user_id
    """))

    op.alter_column("subscriptions", "user_telegram_id", nullable=False)
    op.create_index("ix_subscriptions_user_telegram_id", "subscriptions", ["user_telegram_id"])
    op.create_foreign_key(
        "subscriptions_user_telegram_id_fkey",
        "subscriptions",
        "users",
        ["user_telegram_id"],
        ["telegram_id"],
    )
    op.drop_column("subscriptions", "user_id")

    # ── users ──
    op.drop_constraint("ck_users_telegram_or_email", "users", type_="check")
    op.drop_index("ix_users_email", "users")
    op.drop_column("users", "email")
    op.alter_column("users", "telegram_id", nullable=False)
