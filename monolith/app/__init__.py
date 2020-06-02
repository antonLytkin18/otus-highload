from flask import Flask
from flask_injector import FlaskInjector
from flask_mysqldb import MySQL

from app.auth.views import auth, login_manager
from app.config import Config
from app.dependencies import configure
from app.follower.views import follower
from app.main.views import main
from app.templates.extenstions.filters import tojson_escaped, form_tojson


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    login_manager.init_app(app)
    register_blueprints(app)
    register_template_filters(app)
    injector = FlaskInjector(app=app, modules=[configure])
    app.injector = injector.injector
    db = app.injector.get(MySQL)
    db.init_app(app)

    return app


def register_template_filters(app):
    app.add_template_filter(tojson_escaped)
    app.add_template_filter(form_tojson)


def register_blueprints(app):
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(follower)
