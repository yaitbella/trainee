"""empty message

Revision ID: ab48785e5b6d
Revises: 
Create Date: 2024-02-11 13:32:02.129987

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab48785e5b6d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pace', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('shooting', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('passing', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('dribbling', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('defending', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('physicality', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.drop_column('physicality')
        batch_op.drop_column('defending')
        batch_op.drop_column('dribbling')
        batch_op.drop_column('passing')
        batch_op.drop_column('shooting')
        batch_op.drop_column('pace')

    # ### end Alembic commands ###