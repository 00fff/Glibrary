from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd08fc3399ae8'
down_revision = 'fa3e95e47be7'
branch_labels = None
depends_on = None


def upgrade():
    # Check if the table exists before attempting to create it
    if not op.get_bind().dialect.has_table(op.get_bind(), 'user_to_user_association'):
        op.create_table(
            'user_to_user_association',
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('friend_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['friend_id'], ['user.user_id']),
            sa.ForeignKeyConstraint(['user_id'], ['user.user_id']),
            sa.PrimaryKeyConstraint('user_id', 'friend_id')
        )

    op.drop_table('_alembic_tmp_user')


def downgrade():
    # Check if the table exists before attempting to create it
    if not op.get_bind().dialect.has_table(op.get_bind(), '_alembic_tmp_user'):
        op.create_table(
            '_alembic_tmp_user',
            sa.Column('username', sa.VARCHAR(length=150), nullable=False),
            sa.Column('email', sa.VARCHAR(length=150), nullable=False),
            sa.Column('password', sa.VARCHAR(length=150), nullable=False),
            sa.Column('description', sa.VARCHAR(length=150), nullable=False),
            sa.Column('user_id', sa.INTEGER(), nullable=False),
            sa.UniqueConstraint('email'),
            sa.UniqueConstraint('username')
        )

    op.drop_table('user_to_user_association')
