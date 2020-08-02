from dataclasses import dataclass, field, asdict
from typing import List

from MySQLdb import Date
from MySQLdb.times import DateTimeType
from flask_login import UserMixin


@dataclass()
class Model:

    def as_dict(self):
        return {k: self._format_value(v) for k, v in asdict(self).items() if k not in self.get_related_properties()}

    @staticmethod
    def _format_value(value):
        if isinstance(value, Date):
            return value.__str__()
        return value

    @classmethod
    def get_properties(cls):
        return [v for v in cls.__annotations__ if v not in cls.get_related_properties()]

    @staticmethod
    def get_related_properties():
        return []


@dataclass()
class Follower(Model):
    STATUS_SENT = 1
    STATUS_ACCEPTED = 2

    id: int = None
    follower_user_id: int = None
    followed_user_id: int = None
    status: int = None

    def is_sent(self, user_id: int) -> bool:
        return all([
            self.follower_user_id == user_id,
            self.status == self.STATUS_SENT
        ])

    def is_received(self, user_id: int) -> bool:
        return all([
            self.followed_user_id == user_id,
            self.status == self.STATUS_SENT
        ])

    def is_accepted(self, user_id: int) -> bool:
        return any([
            self.follower_user_id == user_id,
            self.followed_user_id == user_id
        ]) and self.status == self.STATUS_ACCEPTED


@dataclass()
class User(Model, UserMixin):
    id: int = None
    name: str = None
    last_name: str = None
    email: str = None
    password: str = None
    birth_date: Date = None
    gender: str = None
    interests: str = None
    city: str = None
    followers: List[Follower] = field(default_factory=list)

    def get_follower(self) -> Follower:
        if not self.followers:
            return None
        follower, *_ = self.followers
        return follower

    def get_info(self, user_id) -> dict:
        follower = self.get_follower()
        follower_info = {
            'is_sent': follower.is_sent(user_id) if follower else False,
            'is_received': follower.is_received(user_id) if follower else False,
            'is_friend': follower.is_accepted(user_id) if follower else False,
            'can_send': not follower,
            'is_current': user_id == self.id
        }
        return {**self.as_dict(), **follower_info}

    @staticmethod
    def get_related_properties():
        return ['followers']


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
