from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from injector import inject

from app.consul.services import ServiceDiscovery
from app.db.repositories import UserFollowerRepository

chat = Blueprint('chat', __name__, url_prefix='/chat')


@inject
@chat.route('/', methods=['GET'])
@login_required
def index(user_follower_repository: UserFollowerRepository, service_discovery: ServiceDiscovery):
    followers = user_follower_repository.find_all(
        current_user_id=current_user.id,
        accepted=True
    )

    return render_template(
        'chat-list.html',
        follower_list=[v.get_info(current_user.id) for k, v in followers.items()],
        chat_app_url=service_discovery.get('chat-app').address
    )


@inject
@chat.route('/<user_id>', methods=['GET'])
@login_required
def message_list(user_id, repository: UserFollowerRepository, service_discovery: ServiceDiscovery):
    user = repository.find_one(
        current_user_id=current_user.id,
        user_id=user_id,
        accepted=True
    )
    if not user:
        abort(404)

    return render_template(
        'chat-message-list.html',
        user_id=user.id,
        follower=user.get_info(current_user.id),
        chat_app_url=service_discovery.get('chat-app').address
    )
