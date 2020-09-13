"""create post table

Revision ID: 7c5b7e767653
Revises: 1a138bc611c1
Create Date: 2020-08-22 17:30:29.932226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c5b7e767653'
down_revision = '1a138bc611c1'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    connection.execute('''   
        CREATE TABLE post
        (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            data TEXT NOT NULL,
            date_create DATETIME NOT NULL
        )
    ''')


def downgrade():
    connection = op.get_bind()
    connection.execute('DROP TABLE post')
