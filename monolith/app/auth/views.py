from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import current_user, login_required, logout_user
from injector import inject

from app.auth.forms import AuthForm, RegistrationForm
from app.auth.services import RegistrationService
from app.db.models import User

auth = Blueprint('auth', __name__, url_prefix='/auth')


@inject
@auth.route('/login', methods=['GET', 'POST'])
def login(service: RegistrationService):
    if not request.is_json:
        return render_template('login.html', message=current_user.get_id(), login_url=url_for('auth.login'))
    form = AuthForm(data=request.get_json())
    if not form.validate():
        return {
            'success': False,
            'errors': form.errors,
        }

    # todo:
    user = User()
    form.populate_obj(user)
    success, errors = service.auth(
        email=form.email.data,
        password=form.password.data,
    )
    return {
        'success': success,
        'errors': errors,
    }


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@inject
@auth.route('/register', methods=['GET', 'POST'])
def register(service: RegistrationService):
    if not request.is_json:
        return render_template('register.html', message=current_user.get_id())
    form = RegistrationForm(data=request.get_json())
    if not form.validate():
        return {
            'success': False,
            'errors': form.errors,
        }
    success, errors = service.register(User(
        name=form.name.data,
        last_name=form.lastName.data,
        email=form.email.data,
        password=form.password.data,
        age=form.age.data,
        city=form.city.data,
    ))
    return {
        'success': success,
        'errors': errors,
    }

