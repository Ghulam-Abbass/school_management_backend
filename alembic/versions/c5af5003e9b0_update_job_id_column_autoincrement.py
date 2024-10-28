"""update job id column autoincrement

Revision ID: c5af5003e9b0
Revises: ca93534f18c1
Create Date: 2024-10-24 14:11:33.924920

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c5af5003e9b0'
down_revision: Union[str, None] = 'ca93534f18c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'job_table', 'user_table', ['user_id'], ['id'])
    op.create_foreign_key(None, 'password_reset_table', 'user_table', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'password_reset_table', type_='foreignkey')
    op.drop_constraint(None, 'job_table', type_='foreignkey')
    # ### end Alembic commands ###