from flask import Flask
from flask_injector import FlaskInjector

from app.api.v1.routes import v1

from app.config import Config
from app.consul.consul import init_consul

from app.consul.routes import healthcheck
from app.db.db import DbConnectionPool
from app.dependencies import configure
from app.jwt.jwt import jwt
from app.prometheus.prometheus import metrics


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_blueprints(app)
    injector = FlaskInjector(app=app, modules=[configure])
    app.injector = injector.injector
    db = app.injector.get(DbConnectionPool)
    db.init_app(app)
    jwt.init_app(app)
    init_consul(app)
    metrics.init_app(app)

    return app


def register_blueprints(app):
    app.register_blueprint(v1)
    app.register_blueprint(healthcheck)
