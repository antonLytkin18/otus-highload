"""create chat_message table

Revision ID: 32c6a77b4412
Revises: c6647c996d0d
Create Date: 2020-07-29 17:53:54.133099

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '32c6a77b4412'
down_revision = 'c6647c996d0d'
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
