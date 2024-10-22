"""create password reset table

Revision ID: e033b81d6604
Revises: 57c66268b398
Create Date: 2024-10-22 15:56:36.163442

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e033b81d6604'
down_revision: Union[str, None] = '57c66268b398'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('password_reset_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=100), nullable=True),
    sa.Column('expiry_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_password_reset_table_code'), 'password_reset_table', ['code'], unique=True)
    op.create_index(op.f('ix_password_reset_table_id'), 'password_reset_table', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_password_reset_table_id'), table_name='password_reset_table')
    op.drop_index(op.f('ix_password_reset_table_code'), table_name='password_reset_table')
    op.drop_table('password_reset_table')
    # ### end Alembic commands ###