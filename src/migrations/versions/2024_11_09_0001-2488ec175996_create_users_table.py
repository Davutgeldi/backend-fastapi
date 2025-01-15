"""create users table

Revision ID: 2488ec175996
Revises: 89dfad046614
Create Date: 2024-11-09 00:01:11.498165

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2488ec175996"
down_revision: Union[str, None] = "89dfad046614"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
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