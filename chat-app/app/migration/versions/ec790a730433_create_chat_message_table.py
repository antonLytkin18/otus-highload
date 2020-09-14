"""create chat_message table

Revision ID: ec790a730433
Revises: 64ba6a855933
Create Date: 2020-09-09 22:00:25.550965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec790a730433'
down_revision = '64ba6a855933'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    connection.execute('''   
        CREATE TABLE chat_message
        (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            chat_id INT NOT NULL,
            message TEXT NOT NULL,
            date_create DATETIME NOT NULL
        )
    ''')


def downgrade():
    connection = op.get_bind()
    connection.execute('DROP TABLE chat_message')
