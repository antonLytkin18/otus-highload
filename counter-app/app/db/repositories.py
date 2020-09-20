from injector import inject

from app.db.db import RedisDb


class ChatCounterRepository:
    key_template = 'counter-app:{user_id}_{chat_id}'

    @inject
    def __init__(self, db: RedisDb):
        self.db = db

    def _get_filled_key(self, **kwargs) -> str:
        return self.key_template.format_map({
            'user_id': kwargs.get('user_id', '*'),
            'chat_id': kwargs.get('chat_id', '*'),
        })

    def find_all(self, **kwargs) -> dict:
        keys = list(self.db.connection.scan_iter(match=self._get_filled_key(**kwargs)))
        values = self.db.connection.mget(keys)

        return dict(zip(
            [v.replace(self._get_filled_key(**kwargs, chat_id=''), '') for v in keys],
            [int(v) for v in values if v]
        ))

    def incr(self, user_id, chat_id) -> int:
        return self.db.connection.incr(self._get_filled_key(
            user_id=user_id,
            chat_id=chat_id,
        ))

    def decr(self, user_id, chat_id) -> int:
        return self.db.connection.decr(self._get_filled_key(
            user_id=user_id,
            chat_id=chat_id,
        ))
