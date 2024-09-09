"""create post table

Revision ID: ccd9aa98c4b1
Revises: 
Create Date: 2024-09-06 15:20:04.381657

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ccd9aa98c4b1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable= False, primary_key= True), sa.Column('title',sa.String(), nullable= False))


def downgrade():
    op.drop_table('posts')
    pass
