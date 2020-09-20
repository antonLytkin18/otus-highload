import flask_redis
from flask import Flask
from flask_injector import FlaskInjector

from app.api.v1.routes import v1

from app.config import Config
from app.dependencies import configure
from app.jwt.jwt import jwt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_blueprints(app)
    injector = FlaskInjector(app=app, modules=[configure])
    app.injector = injector.injector
    jwt.init_app(app)

    return app


def register_blueprints(app):
    app.register_blueprint(v1)
