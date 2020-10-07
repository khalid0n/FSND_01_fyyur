"""empty message

Revision ID: bc6236854e0c
Revises: 2bcbf437747f
Create Date: 2020-10-07 06:20:21.724346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc6236854e0c'
down_revision = '2bcbf437747f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Shows', sa.Column('start_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Shows', 'start_time')
    # ### end Alembic commands ###
