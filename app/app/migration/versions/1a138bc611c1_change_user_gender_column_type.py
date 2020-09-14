"""Change user gender column type

Revision ID: 1a138bc611c1
Revises: 32c6a77b4412
Create Date: 2020-08-19 17:27:25.902346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a138bc611c1'
down_revision = '32c6a77b4412'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    connection.execute('''ALTER TABLE user MODIFY gender VARCHAR(1) DEFAULT '' NOT NULL;''')


def downgrade():
    connection = op.get_bind()
    connection.execute('''ALTER TABLE user MODIFY gender CHAR(1) DEFAULT '' NOT NULL;''')
