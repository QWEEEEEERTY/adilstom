"""Initial migrations

Revision ID: 9d2e97a209e2
Revises: e9e5aa12f1c6
Create Date: 2024-12-13 13:36:35.763892

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d2e97a209e2'
down_revision: Union[str, None] = 'e9e5aa12f1c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('logs', 'id',
               existing_type=sa.VARCHAR(length=40),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('logs', 'id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=40),
               existing_nullable=False,
               autoincrement=True)
    # ### end Alembic commands ###