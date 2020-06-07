from dataclasses import dataclass, field, asdict
from typing import List

from flask_login import UserMixin


@dataclass()
class Model:

    def as_dict(self):
        return {k: v for k, v in asdict(self).items() if k not in self.get_relation_properties()}

    @classmethod
    def get_properties(cls):
        return [v for v in cls.__annotations__ if v not in cls.get_relation_properties()]

    @staticmethod
    def get_relation_properties():
        return []


@dataclass()
class Follower(Model):

    STATUS_SENT = 1
    STATUS_ACCEPTED = 2

    id: int = None
    follower_user_id: int = None
    followed_user_id: int = None
    status: int = None


@dataclass()
class User(Model, UserMixin):
    id: int = None
    name: str = None
    last_name: str = None
    email: str = None
    password: str = None
    age: int = None
    gender: str = None
    interests: str = None
    city: str = None
    followers: List[Follower] = field(default_factory=list)

    @staticmethod
    def get_relation_properties():
        return ['followers']

    def to_dict(self):
        as_dict = asdict(self)
        return {column: as_dict[column] for column in as_dict if as_dict[column]}

    def is_request_sent(self, id):
        return any([follower.follower_user_id == int(id) for follower in self.followers])

    def is_request_received(self, id):
        return any([follower.followed_user_id == int(id) for follower in self.followers])

    def can_send(self, id):
        return not self.is_friend(id) and not any([self.is_request_sent(id), self.is_request_received(id)])

    def is_friend(self, id):
        return any([(follower.follower_user_id == int(id) or follower.followed_user_id == int(id)) and follower.status == 2 for follower in self.followers])

    def is_current(self, id):
        return self.id == int(id)
