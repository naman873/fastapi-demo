"""add content column to post table

Revision ID: cd41f75ca94b
Revises: 14913e91e971
Create Date: 2023-09-18 15:50:08.574098

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd41f75ca94b'
down_revision: Union[str, None] = '14913e91e971'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String,nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
