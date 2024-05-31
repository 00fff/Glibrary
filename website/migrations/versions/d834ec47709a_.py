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
    # Add the new column without NOT NULL constraint
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=150), nullable=True))

    # Populate the new column with default values
    op.execute("UPDATE user SET description='' WHERE description IS NULL")

    # Add NOT NULL constraint
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('description', nullable=False)


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###
