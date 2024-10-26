from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = '94252bc6b19f'
down_revision = '595ddc626eda'
branch_labels = None
depends_on = None


def upgrade():
    # Get the connection and the inspector to check if the 'users' table exists
    conn = op.get_bind()
    inspector = inspect(conn)

    # Check if the 'users' table exists
    if 'users' not in inspector.get_table_names():
        # If it does not exist, create the 'users' table
        op.create_table('users',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('username', sa.String(length=20), nullable=False),
            sa.Column('email', sa.String(length=50), nullable=False),
            sa.Column('password_hash', sa.String(length=255), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email'),
            sa.UniqueConstraint('username')
        )

    # Alter the 'tasks' table to add a foreign key to 'users'
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_user_id', 'users', ['user_id'], ['id'])


def downgrade():
    # Drop foreign key and column from 'tasks'
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.drop_constraint('fk_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')

    # Drop the 'users' table
    op.drop_table('users')
