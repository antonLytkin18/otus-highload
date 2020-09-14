from dataclasses import asdict

from flask import Blueprint, request
from flask_cors import cross_origin
from flask_jwt import jwt_required, current_identity
from injector import inject

from app.chat.forms import ChatMessageForm, ChatForm
from app.chat.services import ChatService

v1 = Blueprint('auth', __name__, url_prefix='/api/v1')


@inject
@v1.route('/chats', methods=['GET'])
@cross_origin()
@jwt_required()
def chat_list(service: ChatService):
    chats = service.find_chats(current_identity)

    return {
        'success': True,
        'errors': [],
        'list': [asdict(chat_item) for chat_item in chats]
    }


@inject
@v1.route('/chats', methods=['POST'])
@cross_origin()
@jwt_required()
def chat_create(service: ChatService):
    form = ChatForm(data=request.get_json())

    if not form.validate():
        return {
            'success': False,
            'errors': form.errors,
        }

    chat_item = service.find_or_create_chat(current_identity, form.user_id.data)

    return {
        'success': True,
        'errors': [],
        'item': chat_item.as_dict(),
    }


@inject
@v1.route('chats/<chat_id>/messages', methods=['GET'])
@cross_origin()
@jwt_required()
def chat(chat_id, service: ChatService):
    messages = service.find_messages(chat_id, current_identity)

    return {
        'success': True,
        'errors': [],
        'list': [asdict(v) for v in messages]
    }


@inject
@v1.route('chats/<chat_id>/messages', methods=['POST'])
@cross_origin()
@jwt_required()
def add_message(chat_id, service: ChatService):
    form = ChatMessageForm(data=request.get_json())

    if not form.validate():
        return {
            'success': False,
            'errors': form.errors
        }

    message = service.add_message(chat_id, current_identity, form.message.data)

    return {
        'success': True,
        'errors': [],
        'item': asdict(message)
    }
