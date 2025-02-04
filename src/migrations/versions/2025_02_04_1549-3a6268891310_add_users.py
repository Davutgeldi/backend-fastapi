"""add users

Revision ID: 3a6268891310
Revises: b38c3d0dfe2e
Create Date: 2025-02-04 15:49:25.846471

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3a6268891310"
down_revision: Union[str, None] = "b38c3d0dfe2e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=30), nullable=False),
        sa.Column("last_name", sa.String(length=30), nullable=False),
        sa.Column("patronymic", sa.String(length=30), nullable=True),
        sa.Column("email", sa.String(length=30), nullable=False),
        sa.Column("phone", sa.String(length=15), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("phone"),
    )


def downgrade() -> None:
    op.drop_table("users")
