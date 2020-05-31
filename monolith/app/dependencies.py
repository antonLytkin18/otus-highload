from flask_mysqldb import MySQL
from injector import singleton

from app.auth.services import RegistrationService


def configure(binder):
    binder.bind(RegistrationService, scope=singleton)
    # binder.bind(MySQL, scope=singleton)
