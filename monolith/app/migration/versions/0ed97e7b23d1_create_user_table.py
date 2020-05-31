"""create user table

Revision ID: 0ed97e7b23d1
Revises: 
Create Date: 2020-05-09 15:50:22.126667

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '0ed97e7b23d1'
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
            last_name VARCHAR (32) NOT NULL,
            email VARCHAR(128) NOT NULL,
            age TINYINT UNSIGNED NOT NULL,
            password VARCHAR(128) NOT NULL,
            gender CHAR (1) NOT NULL DEFAULT '',
            interests TEXT NULL,
            city VARCHAR (32) NOT NULL
        )
    ''')


def downgrade():
    connection = op.get_bind()
    connection.execute('DROP TABLE user')
