from flask_mysqldb import MySQL
from injector import singleton

from app.auth.services import RegistrationService
from app.follower.services import FollowerService
from app.db.repositories import UserRepository, FollowerRepository


def configure(binder):
    binder.bind(RegistrationService, scope=singleton)
    binder.bind(FollowerService, scope=singleton)
    binder.bind(UserRepository, scope=singleton)
    binder.bind(FollowerRepository, scope=singleton)
    binder.bind(MySQL, scope=singleton)
