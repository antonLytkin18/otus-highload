from dataclasses import asdict

from flask_mysqldb import MySQL
from injector import inject

from app.db.models import User, Follower


class BaseRepository:

    @inject
    def __init__(self, db: MySQL):
        self.db = db

    def fetchone(self, cursor) -> dict:
        data = cursor.fetchone()
        return dict(zip(self.get_columns(cursor), data)) if data else {}

    def fetchall(self, cursor) -> list:
        data = cursor.fetchall()
        return [dict(zip(self.get_columns(cursor), row)) for row in data] if data else []

    @staticmethod
    def get_columns(cursor) -> list:
        return [col[0] for col in cursor.description]

    def find_one(self, **kwargs):
        columns = ' AND '.join([f'{column}=%s' for column in kwargs])
        cur = self.db.connection.cursor()
        cur.execute(f'SELECT * FROM {self.table_name} WHERE {columns}', kwargs.values())
        data = self.fetchone(cur)
        cur.close()
        return self.model_class(**data) if data else False

    def save(self, model) -> bool:
        cur = self.db.connection.cursor()
        user_data = asdict(model)
        filtered = {column: user_data[column] for column in user_data if user_data[column]}

        columns = ', '.join(filtered.keys())
        values_prepared = ', '.join(len(filtered) * ['%s'])

        if filtered.get('id'):
            values = ', '.join([f'{key} = {value}' for (key, value) in filtered.items() if key != 'id'])
            cur.execute(f'UPDATE {self.table_name} SET {values} WHERE id = %(id)s', {'id': filtered.get('id')})
        else:
            cur.execute(f'INSERT INTO {self.table_name} ({columns}) VALUES ({values_prepared})', filtered.values())

        cur.connection.commit()
        cur.close()
        return True


class UserRepository(BaseRepository):
    table_name = 'user'
    model_class = User

    def find_all(self):
        cur = self.db.connection.cursor()
        cur.execute('SELECT * FROM user')
        result = [User(**data) for data in self.fetchall(cur)]
        cur.close()
        return result


class FollowerRepository(BaseRepository):
    table_name = 'follower'
    model_class = Follower

    def get_all_by_user_id(self, id):
        cur = self.db.connection.cursor()

        cur.execute('''
            SELECT u.*, f.follower_user_id, f.followed_user_id, f.status FROM user u
            LEFT JOIN follower f
            ON (u.id = f.follower_user_id OR u.id = f.followed_user_id)
            AND (f.follower_user_id = %(id)s OR f.followed_user_id = %(id)s)
            WHERE u.id != %(id)s
        ''', {'id': id})

        result = {}
        for item in self.fetchall(cur):
            user_data = {k: v for (k, v) in item.items() if k in User.__annotations__}
            follower_data = {k: v for (k, v) in item.items() if k in Follower.__annotations__}
            user = User(**user_data)
            user = result.get(user.id) if user.id in result else user
            user.followers.append(Follower(**follower_data))
            result[user.id] = user

        cur.close()
        return result

    def get_by_user_id(self, id):
        cur = self.db.connection.cursor()

        cur.execute('''
            SELECT u.*, f.follower_user_id, f.followed_user_id, f.status FROM user u
            INNER JOIN follower f
            ON (u.id = f.follower_user_id OR u.id = f.followed_user_id)
            AND (f.follower_user_id = %(id)s OR f.followed_user_id = %(id)s)
            AND f.status = 2
            WHERE u.id != %(id)s
        ''', {'id': id})

        result = {}
        for item in self.fetchall(cur):
            user_data = {k: v for (k, v) in item.items() if k in User.__annotations__}
            follower_data = {k: v for (k, v) in item.items() if k in Follower.__annotations__}
            user = User(**user_data)
            user = result.get(user.id) if user.id in result else user
            user.followers.append(Follower(**follower_data))
            result[user.id] = user

        cur.close()
        return result

    def find_one_with_follower(self, id, current_user_id):
        cur = self.db.connection.cursor()

        cur.execute('''
            SELECT u.*, f.follower_user_id, f.followed_user_id, f.status FROM user u
            LEFT JOIN follower f
            ON (u.id = f.follower_user_id OR u.id = f.followed_user_id)
            AND (f.follower_user_id = %(current_user_id)s OR f.followed_user_id = %(current_user_id)s)
            WHERE u.id = %(id)s
        ''', {'id': id, 'current_user_id': current_user_id})

        result = {}
        item = self.fetchone(cur)
        user_data = {k: v for (k, v) in item.items() if k in User.__annotations__}
        follower_data = {k: v for (k, v) in item.items() if k in Follower.__annotations__}
        user = User(**user_data)
        user = result.get(user.id) if user.id in result else user
        user.followers.append(Follower(**follower_data))

        cur.close()
        return user
