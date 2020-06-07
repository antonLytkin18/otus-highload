from flask import Blueprint, abort, render_template, url_for, request
from flask_login import login_required, current_user
from injector import inject

from app.db.models import Follower
from app.db.repositories import UserRepository, FollowerRepository

follower = Blueprint('follower', __name__, url_prefix='/follower')


@inject
@follower.route('/<user_id>', methods=['GET'])
@login_required
def index(user_id, repository: UserRepository):
    user = repository.find_one_with_follower(current_user.id, int(user_id))
    if not user:
        abort(404)

    users = repository.find_all_with_follower(user.id, accepted=True)
    return render_template(
        'profile.html',
        title='Profile',
        item=user.get_info(current_user.id),
        followers=[v.get_info(user_id) for k, v in users.items()],
    )


@inject
@follower.route('/list', methods=['GET'])
@login_required
def list_accepted(repository: UserRepository):
    users = repository.find_all_with_follower(current_user.id, accepted=True)
    return render_template(
        'users-list.html',
        title='People',
        list=[v.get_info(current_user.id) for k, v in users.items()],
    )


@inject
@follower.route('/list/all', methods=['GET'])
@login_required
def list_all(user_repository: UserRepository):
    users = user_repository.find_all_with_follower(current_user.id)
    return render_template(
        'users-list.html',
        title='People',
        list=[v.get_info(current_user.id) for k, v in users.items()],
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
