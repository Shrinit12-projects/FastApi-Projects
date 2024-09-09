"""add content column to post table

Revision ID: 34ee208b9dc6
Revises: ccd9aa98c4b1
Create Date: 2024-09-06 15:29:58.204623

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34ee208b9dc6'
down_revision: Union[str, None] = 'ccd9aa98c4b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass