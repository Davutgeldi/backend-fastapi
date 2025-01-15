"""updated table rooms

Revision ID: d58b38d811f8
Revises: 2488ec175996
Create Date: 2024-11-15 01:24:11.061385

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d58b38d811f8"
down_revision: Union[str, None] = "2488ec175996"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "rooms",
        "price",
        existing_type=sa.INTEGER(),
        type_=sa.Float(),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "rooms",
        "price",
        existing_type=sa.Float(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )