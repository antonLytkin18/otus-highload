from flask import Blueprint
from injector import inject

from app.db.db import Db

healthcheck = Blueprint('healthcheck', __name__, url_prefix='/')

@inject
@healthcheck.route('/healthcheck', methods=['GET'])
def health(db: Db):
    try:
        db.connection.query('SELECT 1')
    except Exception as e:
        return str(e), 500
    return 'OK', 200
