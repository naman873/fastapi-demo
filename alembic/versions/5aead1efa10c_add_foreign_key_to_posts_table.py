"""add foreign-key to posts table

Revision ID: 5aead1efa10c
Revises: a835a9e29f25
Create Date: 2023-09-18 16:07:27.270978

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5aead1efa10c'
down_revision: Union[str, None] = 'a835a9e29f25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer,nullable=False))
    op.create_foreign_key('post_users_fk',source_table="posts",referent_table="users",local_cols=["owner_id"],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk',table_name="posts")
    op.drop_column('posts',"owner_id")
    pass
