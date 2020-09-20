from flask import Blueprint

from injector import inject

from app.db.repositories import ChatCounterRepository

v1 = Blueprint('v1', __name__, url_prefix='/api/v1')


@inject
@v1.route('/user/<user_id>/chats', methods=['GET'])
def chat_count_list(user_id, repository: ChatCounterRepository):
    try:
        items = repository.find_all(user_id=user_id)
    except Exception as e:
        return {
            'success': False,
            'errors': [str(e)],
            'items': [],
        }

    return {
        'success': True,
        'errors': [],
        'items': items,
    }


@inject
@v1.route('/chat/<chat_id>/messages/<user_id>/incr', methods=['POST'])
def incr(chat_id, user_id, repository: ChatCounterRepository):
    try:
        count = repository.incr(user_id, chat_id)
    except Exception as e:
        return {
            'success': False,
            'errors': [str(e)],
            'count': None,
        }

    return {
        'success': True,
        'errors': [],
        'count': count,
    }


@inject
@v1.route('/chat/<chat_id>/messages/<user_id>/decr', methods=['POST'])
def decr(chat_id, user_id, repository: ChatCounterRepository):
    try:
        count = repository.decr(user_id, chat_id)
    except Exception as e:
        return {
            'success': False,
            'errors': [str(e)],
            'count': None,
        }

    return {
        'success': True,
        'errors': [],
        'count': count,
    }
