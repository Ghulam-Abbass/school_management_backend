"""Add bio field to User model

Revision ID: c37ffec22dc0
Revises: 0793c1abbf76
Create Date: 2024-10-24 12:16:10.563862

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c37ffec22dc0'
down_revision: Union[str, None] = '0793c1abbf76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'password_reset_table', 'user_table', ['user_id'], ['id'])
    op.add_column('user_table', sa.Column('bio', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_table', 'bio')
    op.drop_constraint(None, 'password_reset_table', type_='foreignkey')
    # ### end Alembic commands ###