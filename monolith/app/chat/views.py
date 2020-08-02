from dataclasses import asdict

from flask import Blueprint, render_template, abort, request
from flask_login import login_required, current_user
from injector import inject

from app.chat.forms import ChatMessageForm
from app.chat.services import ChatService
from app.db.repositories import UserFollowerRepository

chat = Blueprint('chat', __name__, url_prefix='/chat')


@inject
@chat.route('/', methods=['GET'])
@login_required
def index(user_follower_repository: UserFollowerRepository, service: ChatService):
    followers = user_follower_repository.find_all(
        current_user_id=current_user.id,
        accepted=True
    )
    chats = service.find_chats(current_user.id)

    return render_template(
        'chat-list.html',
        follower_list=[v.get_info(current_user.id) for k, v in followers.items()],
        chat_list=[asdict(v) for v in chats]
    )


@inject
@chat.route('/<user_id>', methods=['GET'])
@login_required
def message_list(user_id, repository: UserFollowerRepository, service: ChatService):
    user = repository.find_one(
        current_user_id=current_user.id,
        user_id=user_id,
        accepted=True
    )
    if not user:
        abort(404)

    chat = service.find_or_create_chat(current_user.id, user.id)
    messages = service.find_messages(chat.id, current_user.id)

    return render_template(
        'chat-message-list.html',
        chat_id=chat.id,
        list=[asdict(v) for v in messages],
        follower=user.get_info(current_user.id)
    )


@inject
@chat.route('/message/<chat_id>', methods=['POST'])
@login_required
def add_message(chat_id, service: ChatService):
    form = ChatMessageForm(data=request.get_json())
    if not form.validate():
        return {'success': False, 'errors': form.errors}

    message = service.add_message(chat_id, current_user.id, form.message.data)

    return {'success': True, 'message': asdict(message)}
