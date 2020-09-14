from blinker import signal
from flask_login import login_user
from injector import inject
from werkzeug.security import generate_password_hash, check_password_hash

from app.db.models import User
from app.db.repositories import UserRepository


class RegistrationService:

    @inject
    def __init__(self, repository: UserRepository):
        self.repository = repository
        pass

    def auth(self, **kwargs):
        user = self.repository.find_one(email=kwargs['email'])
        if not user:
            return False, ['User doesn\'t exists']
        if not check_password_hash(user.password, kwargs['password']):
            return False, ['User doesn\'t exists']
        login_user(user)
        return True, []

    def register(self, user: User):
        if self.repository.find_one(email=user.email):
            return False, ['User already exists']
        user.password = generate_password_hash(user.password)
        success = self.repository.save(user)
        if success:
            user_registered = signal('user-registered')
            user_registered.send(self, user=user)
        return success, []
