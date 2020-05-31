from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user

main = Blueprint('main', __name__, url_prefix='/')

@main.route('/')
@login_required
def index():
    return redirect(url_for('follower.index', id=current_user.get_id()))
