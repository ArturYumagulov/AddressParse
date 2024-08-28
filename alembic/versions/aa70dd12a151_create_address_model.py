"""create address model

Revision ID: aa70dd12a151
Revises: c65ccd4fec38
Create Date: 2024-08-28 16:00:49.765292

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'aa70dd12a151'
down_revision: Union[str, None] = 'c65ccd4fec38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('addresses',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('code', sa.String(), nullable=False),
                    sa.Column('chicago_code', sa.BigInteger(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('ya_name', sa.String(), nullable=False),
                    sa.Column('category', sa.String(), nullable=False),
                    sa.Column('address', sa.String(), nullable=False),
                    sa.Column('full_address', sa.String(), nullable=False),
                    sa.Column('phone', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('type', sa.String(), nullable=False),
                    sa.Column('department', sa.String(), nullable=False),
                    sa.Column('request_address', sa.String(), nullable=False),
                    sa.Column('country_code', sa.String(length=10), nullable=False),
                    sa.Column('formatted', sa.String(), nullable=False),
                    sa.Column('zip_code', sa.String(), nullable=False),
                    sa.Column('country', sa.String(), nullable=False),
                    sa.Column('province1', sa.String(), nullable=False),
                    sa.Column('province2', sa.String(), nullable=False),
                    sa.Column('city', sa.String(), nullable=False),
                    sa.Column('street', sa.String(), nullable=False),
                    sa.Column('house_number', sa.String(), nullable=False),
                    sa.Column('latitude', sa.String(), nullable=False),
                    sa.Column('longitude', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('addresses')
    # ### end Alembic commands ###
