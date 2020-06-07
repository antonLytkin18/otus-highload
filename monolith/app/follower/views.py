import json

from flask import Blueprint, abort, render_template, url_for, request
from flask_login import login_required, current_user
from injector import inject

from app.db.models import Follower
from app.db.repositories import UserRepository, FollowerRepository

follower = Blueprint('follower', __name__, url_prefix='/follower')


@inject
@follower.route('/<id>', methods=['GET'])
@login_required
def index(id, repository: UserRepository):
    user = repository.find_one(id=id)
    if not user:
        abort(404)

    current_user_id = current_user.id
    user = repository.find_one_with_follower(current_user_id, int(id))
    followers = repository.find_all_with_accepted_follower(current_user_id)
    return render_template(
        'profile.html',
        title='Profile',
        item={
            'id': user.id,
            'name': user.name,
            'last_name': user.last_name,
            'age': user.age,
            'city': user.city,
            'is_sent': user.is_request_sent(current_user_id),
            'is_received': user.is_request_received(current_user_id),
            'can_send': user.can_send(current_user_id),
            'is_friend': user.is_friend(current_user_id),
            'is_current': user.is_current(current_user_id)
        },
        followers=[{
            'id': v.id,
            'name': v.name,
            'age': v.age,
            'city': v.city,
            'is_sent': v.is_request_sent(id),
            'is_received': v.is_request_received(id),
            'can_send': v.can_send(id),
            'is_friend': v.is_friend(id)
        } for (k, v) in followers.items()],
        urls={
            'request': url_for('follower.add'),
            'accept': url_for('follower.accept'),
            'profile': url_for('follower.index', id=':id')
        }
    )


@inject
@follower.route('/list', methods=['GET'])
@login_required
def list(repositiry: UserRepository):
    id = current_user.get_id()
    list = repositiry.find_all_with_accepted_follower(int(id))
    return render_template(
        'users-list.html',
        title='People',
        list=json.dumps([{
            'id': v.id,
            'name': v.name,
            'age': v.age,
            'city': v.city,
            'is_sent': v.is_request_sent(id),
            'is_received': v.is_request_received(id),
            'can_send': v.can_send(id),
            'is_friend': v.is_friend(id),
            'is_current': v.is_current(id)
        } for (k, v) in list.items()]),
        urls=json.dumps({
            'request': url_for('follower.add'),
            'accept': url_for('follower.accept'),
            'profile': url_for('follower.index', id=':id')
        })
    )


@inject
@follower.route('/list/all', methods=['GET', 'POST'])
@login_required
def list_all(user_repository: UserRepository):
    if not request.is_json:
        id = current_user.get_id()
        list = user_repository.find_all_with_follower(id)
        return render_template(
            'users-list.html',
            title='People',
            list=json.dumps([{
                'id': v.id,
                'name': v.name,
                'age': v.age,
                'city': v.city,
                'is_sent': v.is_request_sent(id),
                'is_received': v.is_request_received(id),
                'can_send': v.can_send(id),
                'is_friend': v.is_friend(id),
                'is_current': v.is_current(id)
            } for (k, v) in list.items()]),
            urls=json.dumps({
                'request': url_for('follower.add'),
                'accept': url_for('follower.accept'),
                'profile': url_for('follower.index', id=':id')
            })
        )


@inject
@follower.route('/add', methods=['POST'])
@login_required
def add(repository: FollowerRepository):
    data = request.get_json()
    repository.save(Follower(
        follower_user_id=current_user.get_id(),
        followed_user_id=data['id'],
        status=1
    ))
    return {
        'success': True,
        'errors': [],
    }


@inject
@follower.route('/accept', methods=['POST'])
@login_required
def accept(repository: FollowerRepository):
    data = request.get_json()
    follower = repository.find_one(
        follower_user_id=data['id'],
        followed_user_id=current_user.get_id(),
        status=1
    )
    if not follower:
        return {
            'success': False,
            'errors': [],
        }
    follower.status = 2
    repository.save(follower)

    return {
        'success': True,
        'errors': [],
    }
