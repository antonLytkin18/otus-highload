import json

from blinker import signal
from flask import current_app

from app.db.models import User
from app.db.repositories import UserRepository

user_registered = signal('user-registered')


@user_registered.connect
def register_user(ch, **kwargs):
    payload = json.loads(kwargs.get('body'))
    repository: UserRepository = current_app.injector.get(UserRepository)
    repository.save(User(
        name=payload['name'],
        last_name=payload['last_name']
    ))
