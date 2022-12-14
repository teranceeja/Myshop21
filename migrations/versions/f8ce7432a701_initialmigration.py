"""initialmigration

Revision ID: f8ce7432a701
Revises: 
Create Date: 2022-12-06 22:43:57.681516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8ce7432a701'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('register', schema=None) as batch_op:
        batch_op.add_column(sa.Column('f_name', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('register', schema=None) as batch_op:
        batch_op.drop_column('f_name')

    # ### end Alembic commands ###
