"""create feed table

Revision ID: 4c1ed9483d5e
Revises: 7c5b7e767653
Create Date: 2020-08-22 17:30:39.162376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c1ed9483d5e'
down_revision = '7c5b7e767653'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    connection.execute('''   
        CREATE TABLE feed
        (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            post_id INT NOT NULL,
            date_create DATETIME NOT NULL
        )
    ''')


def downgrade():
    connection = op.get_bind()
    connection.execute('DROP TABLE feed')
