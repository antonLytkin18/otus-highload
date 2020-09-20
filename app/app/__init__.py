from flask import Flask
from flask_injector import FlaskInjector

from app.auth.views import auth, login_manager
from app.broker.broker import AppBroker
from app.cmd.user import user_cmd
from app.config import Config
from app.consul import consul
from app.db.db import DbConnectionPool
from app.dependencies import configure
from app.chat.views import chat
from app.follower.views import follower
from app.jwt.jwt import jwt
from app.main.views import main
from app.feed.views import feed
from app.templates.extenstions.filters import tojson_escaped, form_tojson


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    login_manager.init_app(app)
    register_blueprints(app)
    register_template_filters(app)
    injector = FlaskInjector(app=app, modules=[configure])
    app.injector = injector.injector
    db: DbConnectionPool = app.injector.get(DbConnectionPool)
    db.init_app(app)
    jwt.init_app(app)
    broker: AppBroker = app.injector.get(AppBroker)
    broker.init_app(app)
    consul.init_app(app)

    return app


def register_template_filters(app):
    app.add_template_filter(tojson_escaped)
    app.add_template_filter(form_tojson)


def register_blueprints(app):
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(follower)
    app.register_blueprint(user_cmd)
    app.register_blueprint(chat)
    app.register_blueprint(feed)
