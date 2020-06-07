from flask import Blueprint, abort, render_template, url_for, request
from flask_login import login_required, current_user
from injector import inject

from app.db.repositories import UserRepository
from app.follower.exceptions import FollowerAlreadyExistsException, FollowerDoesNotExistsException
from app.follower.services import FollowerService

follower = Blueprint('follower', __name__, url_prefix='/follower')


@inject
@follower.route('/<user_id>', methods=['GET'])
@login_required
def index(user_id, repository: UserRepository):
    user = repository.find_one_with_follower(current_user.id, int(user_id))
    if not user:
        abort(404)

    users = repository.find_all_with_follower(user.id, accepted=True)
    return render_template('follower.html',
        item=user.get_info(current_user.id),
        followers=[v.get_info(user_id) for k, v in users.items()],
    )


@inject
@follower.route('/list', methods=['GET'])
@login_required
def list_accepted(repository: UserRepository):
    users = repository.find_all_with_follower(current_user.id, accepted=True)
    return render_template('follower-list.html',
        title='Followers',
        list=[v.get_info(current_user.id) for k, v in users.items()],
    )


@inject
@follower.route('/list/all', methods=['GET'])
@login_required
def list_all(user_repository: UserRepository):
    users = user_repository.find_all_with_follower(current_user.id)
    return render_template('follower-list.html',
        title='Profiles',
        list=[v.get_info(current_user.id) for k, v in users.items()],
    )


@inject
@follower.route('/send/<user_id>', methods=['POST'])
@login_required
def send(user_id, repository: UserRepository, service: FollowerService):
    user = repository.find_one(id=user_id)
    if not user:
        abort(404)
    try:
        service.send(current_user, user)
    except FollowerAlreadyExistsException as e:
        return {'success': False, 'errors': [(str(e))]}
    return {'success': True, 'errors': []}


@inject
@follower.route('/accept/<user_id>', methods=['POST'])
@login_required
def accept(user_id, repository: UserRepository, service: FollowerService):
    user = repository.find_one(id=user_id)
    if not user:
        abort(404)
    try:
        service.accept(current_user, user)
    except FollowerDoesNotExistsException as e:
        return {'success': False, 'errors': [(str(e))]}
    return {'success': True, 'errors': []}
