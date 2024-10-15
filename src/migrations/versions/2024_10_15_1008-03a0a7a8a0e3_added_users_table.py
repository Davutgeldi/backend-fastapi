"""added users table

Revision ID: 03a0a7a8a0e3
Revises: 28ef4b9b014e
Create Date: 2024-10-15 10:08:32.905834

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "03a0a7a8a0e3"
down_revision: Union[str, None] = "28ef4b9b014e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "Users",
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
    op.drop_table("Users")
