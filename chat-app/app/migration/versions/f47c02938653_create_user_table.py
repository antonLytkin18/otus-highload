"""create user table

Revision ID: f47c02938653
Revises: 
Create Date: 2020-09-09 21:58:04.594541

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f47c02938653'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    connection.execute('''
        CREATE TABLE user
        (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR (32) NOT NULL,
            last_name VARCHAR (32) NOT NULL
        )
    ''')


def downgrade():
    connection = op.get_bind()
    connection.execute('DROP TABLE user')
