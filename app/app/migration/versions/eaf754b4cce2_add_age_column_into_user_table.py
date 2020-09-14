"""add age column into user table

Revision ID: eaf754b4cce2
Revises: 4c1ed9483d5e
Create Date: 2020-08-30 18:43:16.390626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eaf754b4cce2'
down_revision = '4c1ed9483d5e'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    connection.execute('ALTER TABLE user ADD COLUMN age INT')


def downgrade():
    connection = op.get_bind()
    connection.execute('ALTER TABLE user DROP COLUMN age')
