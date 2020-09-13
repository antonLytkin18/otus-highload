from abc import ABC, abstractmethod

from injector import inject

from app.db.db import Db
from app.db.models import Model, Chat, ChatMessage, User
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

    def paginate_all(self, limit=10, page=1, **kwargs) -> Pagination:
        offset = (page - 1) * limit
        items = self.find_all(limit=limit, offset=offset, **kwargs)
        count = self.count_all(**kwargs)
        return Pagination(per_page=limit, page=page, count=count, list=items)

    @abstractmethod
    def save(self, model: Model) -> bool:
        pass


class BaseMysqlRepository(BaseRepository, ABC):
    table_name = None
    model_class = None

    @inject
    def __init__(self, db: Db):
        self.db = db

    def _fetchone(self, cursor) -> dict:
        data = cursor.fetchone()
        return dict(zip(self._get_columns(cursor), data)) if data else {}

    def _fetchall(self, cursor) -> list:
        data = cursor.fetchall()
        return [dict(zip(self._get_columns(cursor), row)) for row in data] if data else []

    @staticmethod
    def _get_columns(cursor) -> list:
        return [col[0] for col in cursor.description]

    @staticmethod
    def _build_limit_statement(limit: int, offset: int = None) -> str:
        if not limit:
            return ''
        limit_statement = f'LIMIT {limit}'
        limit_statement += f' OFFSET {offset}' if offset else ''
        return limit_statement


class CommonMysqlRepository(BaseMysqlRepository):
    count_alias = 'cnt'

    def _build_query(self, **kwargs):
        limit = kwargs.pop('limit', None)
        offset = kwargs.pop('offset', None)
        select_clause = f'COUNT(id) {self.count_alias}' if kwargs.pop('select_count', False) else '*'
        order_by_clause = kwargs.pop('order_by', False)
        order_statement = f'ORDER BY {order_by_clause}' if order_by_clause else ''
        where_conditions = ' AND '.join([f'{column}=%({column})s' for column in kwargs])
        where_statement = f'WHERE {where_conditions}' if where_conditions else ''
        limit_statement = self._build_limit_statement(limit, offset)
        return f'SELECT {select_clause} FROM {self.table_name} {where_statement} {order_statement} {limit_statement}'

    def find_one(self, **kwargs) -> Model:
        with self.db.connection.cursor() as cursor:
            cursor.execute(self._build_query(**kwargs), kwargs)
            data = self._fetchone(cursor)
        return self.model_class(**data) if data else False

    def find_all(self, **kwargs) -> list:
        with self.db.connection.cursor() as cursor:
            cursor.execute(self._build_query(**kwargs), kwargs)
            data = self._fetchall(cursor)
        return [self.model_class(**item) for item in data]

    def count_all(self, **kwargs) -> int:
        with self.db.connection.cursor() as cursor:
            cursor.execute(self._build_query(select_count=True, **kwargs), kwargs)
            data = self._fetchone(cursor)
        return int(data[self.count_alias]) if self.count_alias in data else 0

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
            last_id_result = self._fetchone(cursor)
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


class ChatRepository(CommonMysqlRepository):
    table_name = 'chat'
    model_class = Chat


class ChatMessageRepository(CommonMysqlRepository):
    table_name = 'chat_message'
    model_class = ChatMessage
