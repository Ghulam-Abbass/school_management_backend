"""Update columns name for job table

Revision ID: 7d81de471452
Revises: 0a0701730458
Create Date: 2024-10-24 12:44:17.697145

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '7d81de471452'
down_revision: Union[str, None] = '0a0701730458'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job_table', sa.Column('job_id', sa.Integer(), nullable=False))
    op.add_column('job_table', sa.Column('job_name', sa.String(length=100), nullable=True))
    op.drop_index('ix_job_table_id', table_name='job_table')
    op.drop_index('ix_job_table_jobe_name', table_name='job_table')
    op.create_index(op.f('ix_job_table_job_id'), 'job_table', ['job_id'], unique=False)
    op.create_index(op.f('ix_job_table_job_name'), 'job_table', ['job_name'], unique=True)
    op.drop_column('job_table', 'jobe_name')
    op.drop_column('job_table', 'id')
    op.create_foreign_key(None, 'password_reset_table', 'user_table', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'password_reset_table', type_='foreignkey')
    op.add_column('job_table', sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False))
    op.add_column('job_table', sa.Column('jobe_name', mysql.VARCHAR(length=100), nullable=True))
    op.drop_index(op.f('ix_job_table_job_name'), table_name='job_table')
    op.drop_index(op.f('ix_job_table_job_id'), table_name='job_table')
    op.create_index('ix_job_table_jobe_name', 'job_table', ['jobe_name'], unique=True)
    op.create_index('ix_job_table_id', 'job_table', ['id'], unique=False)
    op.drop_column('job_table', 'job_name')
    op.drop_column('job_table', 'job_id')
    # ### end Alembic commands ###
