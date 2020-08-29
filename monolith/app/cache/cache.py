import re

from flask import current_app
from redis_cache import CacheDecorator, RedisCache, chunks

from app.db.db import RedisDb


class AppCacheDecorator(CacheDecorator):

    @property
    def client(self):
        return self.__client or current_app.injector.get(RedisDb).connection

    @client.setter
    def client(self, client):
        self.__client = client

    def invalidate_all(self, *args, **kwargs):
        serialized_data = self.serializer([args])[:-2] if args else ''
        serialized_data = re.escape(serialized_data)
        chunks_gen = chunks(self.client.scan_iter(f'{self.prefix}:{self.namespace}:{serialized_data}*'), 500)
        for keys in chunks_gen:
            self.client.delete(*keys)


class AppRedisCache(RedisCache):

    def cache(self, ttl=0, limit=0, namespace=None):
        return AppCacheDecorator(
            redis_client=self.client,
            prefix=self.prefix,
            serializer=self.serializer,
            deserializer=self.deserializer,
            ttl=ttl,
            limit=limit,
            namespace=namespace
        )
