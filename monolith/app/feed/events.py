from blinker import signal

from app.feed.services import FeedService
from app.feed.tasks import update_followers_feed

feed_post_added = signal('feed-post-added')


@feed_post_added.connect
def update_feeds(service: FeedService, **kwargs):
    post = kwargs.get('post')
    update_followers_feed.delay(post.user_id, post.id)
