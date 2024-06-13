"""empty message

Revision ID: fa3e95e47be7
Revises: d834ec47709a
Create Date: 2024-06-01 15:47:13.040843

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa3e95e47be7'
down_revision = 'd834ec47709a'
branch_labels = None
depends_on = None


def upgrade():
    # Check if 'user_game_association' table does not exist before creating it
    conn = op.get_bind()
    if not conn.dialect.has_table(conn, 'user_game_association'):
        op.create_table('user_game_association',
            sa.Column('game_id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.PrimaryKeyConstraint('game_id', 'user_id'),
            sa.ForeignKeyConstraint(['game_id'], ['game.game_id']),
            sa.ForeignKeyConstraint(['user_id'], ['user.user_id'])
        )


def downgrade():
    # Downgrade should drop 'user_game_association' table
    op.drop_table('user_game_association')
