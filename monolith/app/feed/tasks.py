from datetime import datetime

from flask import current_app

from app.db.models import Feed
from app.db.repositories import UserFollowerRepository, FeedRepository, UserRepository
from app.feed.services import FeedService
from app.socketio.socketio import AppSocketIO
from task import celery


@celery.task
def update_followers_feeds(user_id, post_id):
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
        process_follower_feed.delay(follower.id, post_id)


@celery.task
def process_follower_feed(follower_id, post_id):
    injector = current_app.injector
    repository: FeedRepository = injector.get(FeedRepository)
    service: FeedService = injector.get(FeedService)
    io: AppSocketIO = injector.get(AppSocketIO)

    feed = Feed(
        user_id=follower_id,
        post_id=post_id,
        date_create=datetime.now()
    )
    repository.save(feed)
    service.fetch_feed.invalidate_all(follower_id)

    io.connection.emit('feedUpdated', {'userId': follower_id}, room=f'room_{follower_id}')
