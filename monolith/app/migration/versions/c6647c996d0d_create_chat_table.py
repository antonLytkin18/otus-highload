"""create chat table

Revision ID: c6647c996d0d
Revises: 3f7c503e29a6
Create Date: 2020-07-29 17:52:51.400807

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'c6647c996d0d'
down_revision = '3f7c503e29a6'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    connection.execute('''   
        CREATE TABLE chat
        (
            id INT AUTO_INCREMENT PRIMARY KEY,
            from_user_id INT NOT NULL,
            to_user_id INT NOT NULL,
            date_create DATETIME NOT NULL
        )
    ''')


def downgrade():
    connection = op.get_bind()
    connection.execute('DROP TABLE chat')
