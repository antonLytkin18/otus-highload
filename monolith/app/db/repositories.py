from flask_mysqldb import MySQL
from injector import inject

from app.db.models import User, Follower, Model


class BaseRepository:
    table_name = None
    model_class = None

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

    def find_one(self, **kwargs) -> Model:
        where_conditions = ' AND '.join([f'{column}=%({column})s' for column in kwargs])
        where_statement = f'WHERE {where_conditions}' if where_conditions else ''
        with self.db.connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM {self.table_name} {where_statement}', kwargs)
            data = self.fetchone(cursor)
        return self.model_class(**data) if data else False

    def save(self, model: Model) -> bool:
        if model.id:
            return self._update(model)
        return self._insert(model)

    def _insert(self, model: Model) -> bool:
        data = {k: v for k, v in model.as_dict().items() if v is not None}
        columns = ', '.join(data.keys())
        values = ', '.join([f'%({column})s' for column in data.keys()])
        with self.db.connection.cursor() as cursor:
            cursor.execute(f'INSERT INTO {self.table_name} ({columns}) VALUES ({values})', data)
            cursor.connection.commit()
        return True

    def _update(self, model: Model) -> bool:
        data = model.as_dict()
        columns = ', '.join([f'{column} = %({column})s' for column in data.keys() if column != 'id'])
        with self.db.connection.cursor() as cursor:
            cursor.execute(f'UPDATE {self.table_name} SET {columns} WHERE id = %(id)s', data)
            cursor.connection.commit()
        return True

    @staticmethod
    def _build_select(columns: list, alias: str = None) -> str:
        return ', '.join([f'{alias}.{column} {alias}_{column}' if alias else column for column in columns])

    @classmethod
    def _init_model_by_result(cls, result: dict, alias: str, model_cls=None) -> Model:
        model_cls = cls.model_class if model_cls is None else model_cls
        alias_prefix = f'{alias}_'
        properties = {k[len(alias_prefix):]: v for k, v in result.items() if k.startswith(alias_prefix)}
        return model_cls(**properties) if properties.get('id') is not None else None


class UserRepository(BaseRepository):
    table_name = 'user'
    model_class = User
    alias = 'u'
    follower_table_name = 'follower'
    follower_model_class = Follower
    follower_alias = 'f'

    def _build_with_follower_query(self, **kwargs):
        properties = self.model_class.get_properties()
        follower_properties = self.follower_model_class.get_properties()
        where_conditions = ' AND '.join(kwargs['where']) if 'where' in kwargs else None
        where_statement = f'WHERE {where_conditions}' if where_conditions else ''

        return f'''
            SELECT
                {self._build_select(properties, self.alias)},
                {self._build_select(follower_properties, self.follower_alias)}
            FROM
                {self.table_name} {self.alias}
            LEFT JOIN
                {self.follower_table_name} {self.follower_alias}
            ON
                (
                    {self.alias}.id = {self.follower_alias}.follower_user_id
                    OR {self.alias}.id = {self.follower_alias}.followed_user_id
                )
                AND
                (
                    {self.follower_alias}.follower_user_id = %(current_user_id)s
                    OR {self.follower_alias}.followed_user_id = %(current_user_id)s
                )
                AND
                    {self.alias}.id != %(current_user_id)s
            {where_statement}
            ORDER BY
                {self.alias}.id ASC
        '''

    def _create_with_follower_result(self, items: list) -> dict:
        result = {}
        for item in items:
            user = self._init_model_by_result(item, self.alias)
            if not user:
                continue
            user = result[user.id] if user.id in result else user
            follower = self._init_model_by_result(item, self.follower_alias, Follower)
            if follower:
                user.followers.append(follower)
            result[user.id] = user
        return result

    def find_all_with_follower(self, current_user_id, accepted: bool = False) -> dict:
        conditions = []
        search_params = {'current_user_id': current_user_id}
        if accepted:
            conditions.append(f'{self.follower_alias}.status = %(status)s')
            search_params['status'] = self.follower_model_class.STATUS_ACCEPTED
        query = self._build_with_follower_query(where=conditions)
        with self.db.connection.cursor() as cursor:
            cursor.execute(query, search_params)
            items = self.fetchall(cursor)
        return self._create_with_follower_result(items)

    def find_one_with_follower(self, current_user_id: int, user_id: int) -> User:
        query = self._build_with_follower_query(where=[
            f'{self.alias}.id = %(user_id)s',
        ])
        with self.db.connection.cursor() as cursor:
            cursor.execute(query, {
                'current_user_id': current_user_id,
                'user_id': user_id,
            })
            items = self.fetchone(cursor)
        result = self._create_with_follower_result([items])
        return result[user_id] if user_id in result else None


class FollowerRepository(BaseRepository):
    table_name = 'follower'
    model_class = Follower
