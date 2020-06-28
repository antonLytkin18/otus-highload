from flask_mysqldb import MySQL
from injector import inject

from app.db.models import User, Follower, Model
from app.db.utils import Pagination


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
    def _build_select_clause(columns: list, alias: str = None) -> str:
        return ', '.join([f'{alias}.{column} {alias}_{column}' if alias else column for column in columns])

    @staticmethod
    def _build_limit_statement(limit: int, offset: int = None) -> str:
        limit_statement = f'LIMIT {limit}'
        limit_statement += f' OFFSET {offset}' if offset else ''
        return limit_statement

    @classmethod
    def _init_model_by_result(cls, result: dict, alias: str, model_cls=None) -> Model:
        model_cls = cls.model_class if model_cls is None else model_cls
        alias_prefix = f'{alias}_'
        properties = {k[len(alias_prefix):]: v for k, v in result.items() if k.startswith(alias_prefix)}
        return model_cls(**properties) if properties.get('id') is not None else None


class UserRepository(BaseRepository):
    table_name = 'user'
    model_class = User


class FollowerRepository(BaseRepository):
    table_name = 'follower'
    model_class = Follower


class UserFollowerRepository(BaseRepository):
    table_name = 'user'
    model_class = User
    alias = 'u'
    follower_table_name = 'follower'
    follower_model_class = Follower
    follower_alias = 'f'

    @inject
    def __init__(self, db: MySQL, current_user: User):
        super().__init__(db)
        self.current_user = current_user

    def set_current_user(self, current_user: User):
        self.current_user = current_user

    def _build_subquery(self, **kwargs):
        limit = kwargs.get('limit')
        limit_statement = self._build_limit_statement(limit, kwargs.get('offset')) if limit else ''
        return f'(SELECT * FROM {self.table_name} {limit_statement})'

    def _build_query(self, **kwargs):
        if kwargs.get('select_count', False):
            select_clause = f'COUNT(DISTINCT {self.alias}.id) cnt'
        else:
            select_clause = f'''
                {self._build_select_clause(self.model_class.get_properties(), self.alias)},
                {self._build_select_clause(self.follower_model_class.get_properties(), self.follower_alias)}

            '''
        from_clause = kwargs.get('subquery') or self.table_name
        where = kwargs.get('where', [])
        where_statement = f"WHERE {' AND '.join(where)}" if where else ''
        on_clause = f'''
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
        '''
        limit = kwargs.get('limit')
        limit_statement = self._build_limit_statement(limit, kwargs.get('offset')) if limit is not None else ''

        return f'''
            SELECT {select_clause}
            FROM {from_clause} {self.alias}
            LEFT JOIN {self.follower_table_name} {self.follower_alias}
            ON {on_clause}
            {where_statement}
            ORDER BY {self.alias}.id ASC
            {limit_statement}
        '''

    def _create_query(self, **kwargs):
        conditions = []
        search_params = {'current_user_id': self.current_user.id}
        select_count = kwargs.get('select_count', False)
        accepted = kwargs.get('accepted', False)
        user_id = kwargs.get('user_id')
        name_like = kwargs.get('name_like')
        last_name_like = kwargs.get('last_name_like')
        limit = kwargs.get('limit')
        offset = kwargs.get('offset')
        subquery = None

        if accepted:
            conditions.append(f'{self.follower_alias}.status = %(status)s')
            search_params['status'] = self.follower_model_class.STATUS_ACCEPTED

        if user_id:
            conditions.append(f'{self.alias}.id = %(user_id)s')
            search_params['user_id'] = user_id

        if name_like:
            conditions.append(f'{self.alias}.name LIKE %(name_like)s')
            search_params['name_like'] = name_like + '%'
            if last_name_like:
                conditions.append(f'{self.alias}.last_name LIKE %(last_name_like)s')
                search_params['last_name_like'] = last_name_like + '%'

        if not conditions:
            subquery = self._build_subquery(limit=limit, offset=offset)
            limit = offset = None

        if select_count:
            limit = offset = None

        query = self._build_query(
            select_count=select_count,
            subquery=subquery,
            where=conditions,
            limit=limit,
            offset=offset,
        )
        return query, search_params

    def _create_result(self, items: list) -> dict:
        result = {}
        for item in items:
            model = self._init_model_by_result(item, self.alias)
            if not model:
                continue
            model = result[model.id] if model.id in result else model
            follower = self._init_model_by_result(item, self.follower_alias, Follower)
            if follower:
                model.followers.append(follower)
            result[model.id] = model
        return result

    def _find_one_item(self, **kwargs):
        query, search_params = self._create_query(**kwargs)
        with self.db.connection.cursor() as cursor:
            cursor.execute(query, search_params)
            return self.fetchone(cursor)

    def _find_all_items(self, **kwargs):
        query, search_params = self._create_query(**kwargs)
        with self.db.connection.cursor() as cursor:
            cursor.execute(query, search_params)
            return self.fetchall(cursor)

    def find_one(self, **kwargs) -> User:
        item = self._find_one_item(**kwargs)
        result = self._create_result([item])
        if not result:
            return None
        model, *_ = result.values()
        return model

    def find_all(self, **kwargs) -> dict:
        items = self._find_all_items(**kwargs)
        return self._create_result(items)

    def count_all(self, **kwargs) -> int:
        item = self._find_one_item(select_count=True, **kwargs)
        return int(item['cnt']) if 'cnt' in item else 0

    def paginate_all(self, limit=10, page=1, **kwargs) -> Pagination:
        offset = (page - 1) * limit
        items = self.find_all(limit=limit, offset=offset, **kwargs)
        count = self.count_all(**kwargs)
        return Pagination(per_page=limit, page=page, count=count, list=items)
