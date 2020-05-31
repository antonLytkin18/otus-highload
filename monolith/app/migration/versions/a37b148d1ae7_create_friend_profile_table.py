"""create friend_profile table

Revision ID: a37b148d1ae7
Revises: 0ed97e7b23d1
Create Date: 2020-05-09 19:13:42.099836

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'a37b148d1ae7'
down_revision = '0ed97e7b23d1'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    connection.execute('''   
        CREATE TABLE follower
        (
            id INT AUTO_INCREMENT PRIMARY KEY,
            follower_user_id INT NULL,
            followed_user_id INT NULL,
            status TINYINT NOT NULL
        )
    ''')


def downgrade():
    connection = op.get_bind()
    connection.execute('DROP TABLE follower')
