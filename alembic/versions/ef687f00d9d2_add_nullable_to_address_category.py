"""add nullable to address category

Revision ID: ef687f00d9d2
Revises: ee9db9c08a41
Create Date: 2024-10-16 09:54:04.890844

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'ef687f00d9d2'
down_revision: Union[str, None] = 'ee9db9c08a41'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('addresses', 'category',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('addresses', 'category',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    # ### end Alembic commands ###
