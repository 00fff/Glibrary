"""empty message

Revision ID: d834ec47709a
Revises: 
Create Date: 2024-05-30 19:43:39.987464

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd834ec47709a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Check if 'game' table exists before trying to create it
    conn = op.get_bind()
    if not conn.dialect.has_table(conn, 'game'):
        op.create_table('game',
            sa.Column('game_id', sa.Integer(), nullable=False),
            sa.Column('title', sa.String(length=150), nullable=False),
            sa.Column('description', sa.String(length=150), nullable=False),
            sa.Column('art', sa.String(length=150), nullable=False),
            sa.Column('platform', sa.String(length=50), nullable=False),
            sa.Column('genre', sa.String(length=50), nullable=False),
            sa.Column('release_date', sa.Date()),
            sa.Column('developer', sa.String(length=100)),
            sa.Column('publisher', sa.String(length=100)),
            sa.Column('rating', sa.String(length=10)),
            sa.PrimaryKeyConstraint('game_id'),
            sa.UniqueConstraint('title')
        )

def downgrade():
    op.drop_table('game')

    # ### end Alembic commands ###
