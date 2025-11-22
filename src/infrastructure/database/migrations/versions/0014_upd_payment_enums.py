"""upd payment gateway enum

Revision ID: 7ef2197c3bad
Revises: 0013
Create Date: 2025-11-22 15:02:52.494015

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0014'
down_revision: Union[str, None] = '0013'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE payment_gateway_type ADD VALUE 'CRYPTOPAY' AFTER 'HELEKET'")
    op.execute("ALTER TYPE payment_gateway_type ADD VALUE 'ROBOKASSA' AFTER 'CRYPTOPAY'")


def downgrade() -> None:
    op.execute("ALTER TYPE payment_gateway_type DROP ATTRIBUTE IF EXISTS CRYPTOPAY")
    op.execute("ALTER TYPE payment_gateway_type DROP ATTRIBUTE IF EXISTS ROBOKASSA")