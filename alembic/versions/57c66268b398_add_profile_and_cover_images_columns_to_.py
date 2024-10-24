"""add profile and cover images columns to user table

Revision ID: 57c66268b398
Revises: 78951a700fc7
Create Date: 2024-10-22 14:06:44.175321

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57c66268b398'
down_revision: Union[str, None] = '78951a700fc7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_table', sa.Column('profile_image', sa.String(length=255), nullable=True))
    op.add_column('user_table', sa.Column('cover_image', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_table', 'cover_image')
    op.drop_column('user_table', 'profile_image')
    # ### end Alembic commands ###
