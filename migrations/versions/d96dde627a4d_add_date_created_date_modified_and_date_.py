"""Add date_created, date_modified, and date_deleted columns to Task model

Revision ID: d96dde627a4d
Revises: 
Create Date: 2024-10-11 09:20:04.538530

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd96dde627a4d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_created', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('date_modified', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('date_deleted', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.drop_column('date_deleted')
        batch_op.drop_column('date_modified')
        batch_op.drop_column('date_created')

    # ### end Alembic commands ###
