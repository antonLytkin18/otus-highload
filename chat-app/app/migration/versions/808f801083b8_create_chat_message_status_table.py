"""create chat_message_status table

Revision ID: 808f801083b8
Revises: ec790a730433
Create Date: 2020-09-19 18:43:46.727312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '808f801083b8'
down_revision = 'ec790a730433'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    connection.execute('''   
        CREATE TABLE chat_message_status
        (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            chat_message_id INT NOT NULL,
            status VARCHAR(1) DEFAULT '' NOT NULL,
            date_create DATETIME NOT NULL
        )
    ''')


def downgrade():
    connection = op.get_bind()
    connection.execute('DROP TABLE chat_message_status')
