"""empty message

Revision ID: 8156283d77c4
Revises: 02818f61698a
Create Date: 2017-07-26 10:17:17.501567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8156283d77c4'
down_revision = '02818f61698a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('queries', sa.Column('additional_info', sa.String(length=100), nullable=True))
    op.add_column('queries', sa.Column('location', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('queries', 'location')
    op.drop_column('queries', 'additional_info')
    # ### end Alembic commands ###
