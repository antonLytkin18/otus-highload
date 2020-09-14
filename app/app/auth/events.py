import json

from blinker import signal
from flask import current_app

from app.auth.services import RegistrationService
from app.broker.broker import AppBroker
from app.db.models import User

user_registered = signal('user-registered')


@user_registered.connect
def send_user_registered_message(service: RegistrationService, **kwargs):
    broker: AppBroker = current_app.injector.get(AppBroker)
    user: User = kwargs.get('user')
    broker.publish('main-app-user-registered', json.dumps(user.as_dict()))
