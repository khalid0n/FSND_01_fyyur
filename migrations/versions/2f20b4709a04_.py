"""empty message

Revision ID: 2f20b4709a04
Revises: bc6236854e0c
Create Date: 2020-10-07 07:41:47.055831

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f20b4709a04'
down_revision = 'bc6236854e0c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Shows', sa.Column('id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Shows', 'id')
    # ### end Alembic commands ###
