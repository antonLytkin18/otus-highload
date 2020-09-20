from dataclasses import dataclass, asdict

from MySQLdb import Date
from MySQLdb.times import DateTimeType


@dataclass()
class Model:

    def as_dict(self, with_related=False):
        return {k: self._format_value(v) for k, v in asdict(self).items() if
                with_related or k not in self.get_related_properties()}

    @classmethod
    def _format_value(cls, value):
        if isinstance(value, dict):
            return {k: cls._format_value(v) for k, v in value.items()}
        if isinstance(value, Date):
            return value.__format__('%Y-%m-%d %H:%I:%S')
        return value

    @classmethod
    def get_properties(cls):
        return [v for v in cls.__annotations__ if v not in cls.get_related_properties()]

    @staticmethod
    def get_related_properties():
        return []


@dataclass()
class User(Model):
    id: int = None
    name: str = None
    last_name: str = None


@dataclass()
class Chat(Model):
    id: int = None
    from_user_id: int = None
    to_user_id: int = None
    date_create: DateTimeType = None


@dataclass()
class ChatMessage(Model):
    id: int = None
    user_id: int = None
    chat_id: int = None
    message: str = None
    date_create: DateTimeType = None


@dataclass()
class ChatMessageStatus(Model):
    STATUS_NOT_READ = 1
    STATUS_READ = 2

    id: int = None
    user_id: int = None
    chat_message_id: int = None
    status: int = None
    date_create: DateTimeType = None

    @property
    def is_read(self):
        return int(self.status) == self.STATUS_READ

    def set_read_status(self):
        self.status = self.STATUS_READ

    def set_not_read_status(self):
        self.status = self.STATUS_NOT_READ
