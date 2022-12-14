"""customerid

Revision ID: 44085f66cacc
Revises: e430e3a85b95
Create Date: 2022-12-07 15:13:01.233997

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44085f66cacc'
down_revision = 'e430e3a85b95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer_order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('customer_id', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer_order', schema=None) as batch_op:
        batch_op.drop_column('customer_id')

    # ### end Alembic commands ###
