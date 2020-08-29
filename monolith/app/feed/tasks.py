from datetime import datetime

from flask import current_app

from app.db.models import Feed
from app.db.repositories import UserFollowerRepository, FeedRepository, UserRepository
from app.feed.services import FeedService
from task import celery


@celery.task
def update_followers_feed(user_id, post_id):
    injector = current_app.injector
    follower_repository: UserFollowerRepository = injector.get(UserFollowerRepository)
    user_repository: UserRepository = injector.get(UserRepository)
    current_user = user_repository.find_one(id=user_id)
    followers = follower_repository.find_all(
        current_user_id=user_id,
        accepted=True
    )
    followers[current_user.id] = current_user
    for key, follower in followers.items():
        update_follower_feed.delay(follower.id, post_id)


@celery.task
def update_follower_feed(follower_id, post_id):
    repository = current_app.injector.get(FeedRepository)
    service: FeedService = current_app.injector.get(FeedService)
    feed_post = Feed(
        user_id=follower_id,
        post_id=post_id,
        date_create=datetime.now()
    )
    repository.save(feed_post)
    service.fetch_feed.invalidate_all(follower_id)
