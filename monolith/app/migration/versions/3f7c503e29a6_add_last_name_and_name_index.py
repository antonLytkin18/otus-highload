"""add last name and name index

Revision ID: 3f7c503e29a6
Revises: a37b148d1ae7
Create Date: 2020-07-05 19:11:47.528903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f7c503e29a6'
down_revision = 'a37b148d1ae7'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    connection.execute('CREATE INDEX idx_ln_n ON user(last_name, name)')


def downgrade():
    connection = op.get_bind()
    connection.execute('DROP INDEX idx_ln_n ON user')
