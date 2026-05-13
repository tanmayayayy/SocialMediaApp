"""create postss table

Revision ID: 697f29afb9ed
Revises: 
Create Date: 2026-03-28 18:23:29.220894

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '697f29afb9ed'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('postss',sa.Column('id', sa.Integer(), nullable=False, primary_key = True),sa.Column('title',sa.String(),nullable = False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('postss')
    pass
