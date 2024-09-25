"""initial migration

Revision ID: 962f13c5e7c0
Revises: 
Create Date: 2024-09-26 01:36:13.735580

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '962f13c5e7c0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('Hotels',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('city', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
   


def downgrade() -> None:
    op.drop_table('Hotels')