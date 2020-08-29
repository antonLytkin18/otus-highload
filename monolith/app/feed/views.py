from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from injector import inject

from app.feed.forms import FeedPostForm
from app.feed.services import FeedService

feed = Blueprint('feed', __name__, url_prefix='/feed')


@inject
@feed.route('/', defaults={'page': 1}, methods=['GET'])
@feed.route('/<page>', methods=['GET'])
@login_required
def index(page, service: FeedService):
    feed_posts, pagination_params = service.fetch_feed(current_user.id, int(page))

    return render_template(
        'feed.html',
        list=feed_posts,
        pagination=pagination_params if feed_posts else None,
    )


@inject
@feed.route('/post/add', methods=['POST'])
@login_required
def add_post(service: FeedService):
    form = FeedPostForm(data=request.get_json())
    if not form.validate():
        return {'success': False, 'errors': form.errors}
    post = service.add_post(current_user.id, form.message.data)

    return {'success': True, 'message': post.as_dict()}
