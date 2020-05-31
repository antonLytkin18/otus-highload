from flask import url_for
from flask_login import LoginManager
from injector import Injector
from werkzeug.utils import redirect

from app.db.repositories import UserRepository

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id: int):
    injector = Injector()
    repository = injector.get(UserRepository)
    return repository.find_one(id=user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))
