"""Add profile_image to User model

Revision ID: 6beb8c4c8278
Revises: d08fc3399ae8
Create Date: 2024-06-20 16:27:28.962459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6beb8c4c8278'
down_revision = 'd08fc3399ae8'
branch_labels = None
depends_on = None


def upgrade():
    # Add the profile_image column to the user table
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_image', sa.String(length=150), nullable=True))


def downgrade():
    # Drop the profile_image column from the user table, checking if it exists first
    with op.batch_alter_table('user', schema=None) as batch_op:
        if batch_op.has_column('profile_image'):
            batch_op.drop_column('profile_image')
