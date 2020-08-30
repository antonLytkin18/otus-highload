"""add age and gender index into user table

Revision ID: 52aebee3d078
Revises: eaf754b4cce2
Create Date: 2020-08-30 18:56:49.286268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52aebee3d078'
down_revision = 'eaf754b4cce2'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    connection.execute('CREATE INDEX idx_age_gender ON user(age, gender)')


def downgrade():
    connection = op.get_bind()
    connection.execute('DROP INDEX idx_age_gender ON user')
