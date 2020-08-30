from datetime import datetime

from blinker import signal
from flask import current_app
from injector import inject

from app.cache import cache
from app.db.models import Post
from app.db.repositories import PostRepository, FeedRepository, UserRepository


class FeedService:

    @inject
    def __init__(self, post_repository: PostRepository, user_repository: UserRepository):
        self.post_repository = post_repository
        self.user_repository = user_repository

    def add_post(self, user_id: int, data: str):
        post = Post(
            user_id=user_id,
            data=data,
            date_create=datetime.now()
        )
        self.post_repository.save(post)

        post.user = self.user_repository.find_one(id=post.user_id)
        feed_post_added = signal('feed-post-added')
        feed_post_added.send(self, post=post)

        return post

    @staticmethod
    @cache.cache()
    def fetch_feed(user_id: int, page=1):
        injector = current_app.injector
        feed_repository: FeedRepository = injector.get(FeedRepository)
        post_repository: PostRepository = injector.get(PostRepository)
        user_repository: UserRepository = injector.get(UserRepository)

        pagination = feed_repository.paginate_all(user_id=user_id, page=page, order_by='id desc')
        feeds = pagination.list
        for feed in feeds:
            post = post_repository.find_one(id=feed.post_id)
            post.user = user_repository.find_one(id=post.user_id)
            feed.post = post
        return [feed_post.as_dict(True) for feed_post in feeds], pagination.get_params()
