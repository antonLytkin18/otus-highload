from abc import ABC, abstractmethod

from injector import inject

from app.db.db import SlaveDb, ChatShardedDb, Db, TarantoolDb
from app.db.models import User, Follower, Model, Chat, ChatMessage
from app.db.utils import Pagination


class BaseRepository(ABC):
    @abstractmethod
    def find_one(self, **kwargs) -> Model:
        pass

    @abstractmethod
    def find_all(self, **kwargs) -> list:
        pass

    @abstractmethod
    def count_all(self, **kwargs) -> int:
        pass

    @abstractmethod
    def paginate_all(self, limit=10, page=1, **kwargs) -> Pagination:
        pass

    @abstractmethod
    def save(self, model: Model) -> bool:
        pass


class BaseMysqlRepository(BaseRepository, ABC):
    table_name = None
    model_class = None

    @inject
    def __init__(self, db: Db):
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


class BaseTarantoolRepository(BaseRepository):
    space_name = None
    model_class = None
    model_properties = []

    @inject
    def __init__(self, db: TarantoolDb):
        self.db = db

    @property
    def space(self):
        return self.db.connection.space(self.space_name)

    def find_one(self, **kwargs) -> Model:
        pass

    def find_all(self, **kwargs) -> dict:
        items = {}
        for item in self._find_all_callback(**kwargs):
            data = dict(zip(self.model_properties, item))
            model = self.model_class(**data)
            items[model.id] = model
        return items

    def _find_all_callback(self, **kwargs):
        limit = kwargs.get('limit', 10)
        offset = kwargs.get('offset', 0)
        return self.space.select(limit=limit, offset=offset)

    def count_all(self, **kwargs) -> int:
        return self.space.call('count_all', [self.space_name]).data[0]

    def paginate_all(self, limit=10, page=1, **kwargs) -> Pagination:
        offset = (page - 1) * limit
        items = self.find_all(limit=limit, offset=offset, **kwargs)
        count = self.count_all(**kwargs)
        return Pagination(per_page=limit, page=page, count=count, list=items)

    def save(self, model: Model) -> bool:
        pass


class CommonMysqlRepository(BaseMysqlRepository):

    def find_one(self, **kwargs) -> Model:
        order_by_clause = kwargs.pop('order_by', False)
        order_statement = f'ORDER BY {order_by_clause}' if order_by_clause else ''
        where_conditions = ' AND '.join([f'{column}=%({column})s' for column in kwargs])
        where_statement = f'WHERE {where_conditions}' if where_conditions else ''
        with self.db.connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM {self.table_name} {where_statement} {order_statement}', kwargs)
            data = self.fetchone(cursor)
        return self.model_class(**data) if data else False

    def find_all(self, **kwargs) -> list:
        where_conditions = ' AND '.join([f'{column}=%({column})s' for column in kwargs])
        where_statement = f'WHERE {where_conditions}' if where_conditions else ''
        with self.db.connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM {self.table_name} {where_statement}', kwargs)
            data = self.fetchall(cursor)
        return [self.model_class(**item) for item in data]

    def paginate_all(self, limit=10, page=1, **kwargs) -> Pagination:
        pass

    def count_all(self, **kwargs) -> int:
        pass

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
            cursor.execute('SELECT LAST_INSERT_ID()')
            last_id_result = self.fetchone(cursor)
            last_id, *_ = list(last_id_result.values())
            model.id = last_id
            cursor.connection.commit()
        return True

    def _update(self, model: Model) -> bool:
        data = model.as_dict()
        columns = ', '.join([f'{column} = %({column})s' for column in data.keys() if column != 'id'])
        with self.db.connection.cursor() as cursor:
            cursor.execute(f'UPDATE {self.table_name} SET {columns} WHERE id = %(id)s', data)
            cursor.connection.commit()
        return True


class UserRepository(CommonMysqlRepository):
    table_name = 'user'
    model_class = User


class FollowerRepository(CommonMysqlRepository):
    table_name = 'follower'
    model_class = Follower


class UserFollowerRepository(BaseMysqlRepository):
    table_name = 'user'
    model_class = User
    alias = 'u'
    follower_table_name = 'follower'
    follower_model_class = Follower
    follower_alias = 'f'
    count_alias = 'cnt'

    @classmethod
    def _init_model_by_result(cls, result: dict, alias: str, model_cls=None) -> Model:
        model_cls = cls.model_class if model_cls is None else model_cls
        alias_prefix = f'{alias}_'
        properties = {k[len(alias_prefix):]: v for k, v in result.items() if k.startswith(alias_prefix)}
        return model_cls(**properties) if properties.get('id') is not None else None

    @staticmethod
    def _build_select_clause(columns: list, alias: str = None) -> str:
        return ', '.join([f'{alias}.{column} {alias}_{column}' if alias else column for column in columns])

    @staticmethod
    def _build_limit_statement(limit: int, offset: int = None) -> str:
        if not limit:
            return ''
        limit_statement = f'LIMIT {limit}'
        limit_statement += f' OFFSET {offset}' if offset else ''
        return limit_statement

    def _build_subquery(self, **kwargs):
        limit = kwargs.get('limit')
        limit_statement = self._build_limit_statement(limit, kwargs.get('offset'))
        return f'(SELECT * FROM {self.table_name} {limit_statement})'

    def _build_query(self, **kwargs):
        if kwargs.get('select_count', False):
            select_clause = f'COUNT(DISTINCT {self.alias}.id) {self.count_alias}'
        else:
            select_clause = f'''
                {self._build_select_clause(self.model_class.get_properties(), self.alias)},
                {self._build_select_clause(self.follower_model_class.get_properties(), self.follower_alias)}

            '''

        from_clause = self.table_name
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

        where_statement = limit_statement = ''
        conditions = kwargs.get('conditions', [])
        if conditions:
            where_statement = f"WHERE {' AND '.join(conditions)}"
            limit_statement = self._build_limit_statement(kwargs.get('limit'), kwargs.get('offset'))
        else:
            from_clause = self._build_subquery(limit=kwargs.get('limit'), offset=kwargs.get('offset'))

        return f'''
            SELECT {select_clause}
            FROM {from_clause} {self.alias}
            LEFT JOIN {self.follower_table_name} {self.follower_alias}
            ON {on_clause}
            {where_statement}
            ORDER BY {self.alias}.id ASC
            {limit_statement}
        '''

    def _create_query(self, current_user_id: int, **kwargs):
        conditions = []
        search_params = {'current_user_id': current_user_id}
        user_id = kwargs.get('user_id')

        if kwargs.get('accepted', False):
            conditions.append(f'{self.follower_alias}.status = %(status)s')
            search_params['status'] = self.follower_model_class.STATUS_ACCEPTED

        if user_id:
            conditions.append(f'{self.alias}.id = %(user_id)s')
            search_params['user_id'] = user_id

        last_name_like = kwargs.get('last_name_like')
        if last_name_like:
            conditions.append(f'{self.alias}.last_name LIKE %(last_name_like)s')
            search_params['last_name_like'] = last_name_like + '%'

        name_like = kwargs.get('name_like')
        if name_like:
            conditions.append(f'{self.alias}.name LIKE %(name_like)s')
            search_params['name_like'] = name_like + '%'

        query = self._build_query(
            select_count=kwargs.get('select_count', False),
            conditions=conditions,
            limit=kwargs.get('limit'),
            offset=kwargs.get('offset'),
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
        return int(item[self.count_alias]) if self.count_alias in item else 0

    def paginate_all(self, limit=10, page=1, **kwargs) -> Pagination:
        offset = (page - 1) * limit
        items = self.find_all(limit=limit, offset=offset, **kwargs)
        count = self.count_all(**kwargs)
        return Pagination(per_page=limit, page=page, count=count, list=items)

    def save(self, model: Model) -> bool:
        pass


class UserFollowerReadOnlyRepository(UserFollowerRepository):

    @inject
    def __init__(self, db: SlaveDb):
        super().__init__(db)

    def save(self, model: Model) -> bool:
        raise Exception('Cannot make write operations in read-only repository')


class ChatRepository(CommonMysqlRepository):
    table_name = 'chat'
    model_class = Chat


class ChatMessageRepository(CommonMysqlRepository):
    table_name = 'chat_message'
    model_class = ChatMessage


class ChatMessageShardedRepository(ChatMessageRepository):
    @inject
    def __init__(self, db: ChatShardedDb):
        super().__init__(db)


class UserTarantoolRepository(BaseTarantoolRepository):
    space_name = '513'
    model_class = User
    model_properties = ['id', 'name', 'last_name', 'email', 'birth_date', 'password', 'gender', 'interests', 'city']

    def _find_all_callback(self, **kwargs):
        limit = kwargs.get('limit', 10)
        offset = kwargs.get('offset', 0)
        last_name_like = kwargs.get('last_name_like') or ''
        name_like = kwargs.get('name_like') or ''
        return self.space.call('follower_find_all', [last_name_like, name_like, limit, offset]).data[0]

    def count_all(self, **kwargs) -> int:
        last_name_like = kwargs.get('last_name_like') or ''
        name_like = kwargs.get('name_like') or ''
        return self.space.call('follower_count_all', [last_name_like, name_like]).data[0]
