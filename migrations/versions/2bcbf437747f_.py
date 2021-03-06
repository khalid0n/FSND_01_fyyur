"""empty message

Revision ID: 2bcbf437747f
Revises: 012bd2dd1f71
Create Date: 2020-10-06 13:59:19.098726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bcbf437747f'
down_revision = '012bd2dd1f71'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'address')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('address', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
