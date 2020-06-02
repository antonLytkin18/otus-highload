from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required, logout_user
from injector import inject

from app.auth.forms import AuthForm, RegistrationForm
from app.auth.services import RegistrationService
from app.db.models import User

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html', form=AuthForm())


@inject
@auth.route('/login', methods=['POST'])
def login(service: RegistrationService):
    form = AuthForm(data=request.get_json())
    if not form.validate():
        return {'success': False, 'errors': form.errors}

    success, errors = service.auth(
        email=form.email.data,
        password=form.password.data,
    )
    if errors:
        form.email.errors.append(errors)
    return {'success': success, 'errors': form.errors}


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html', form=RegistrationForm())


@inject
@auth.route('/register', methods=['POST'])
def register(service: RegistrationService):
    form = RegistrationForm(data=request.get_json())
    if not form.validate():
        return {'success': False, 'errors': form.errors}
    user = User()
    form.populate_obj(user)
    success, errors = service.register(user)
    if errors:
        form.email.errors.append(errors)
    return {'success': success, 'errors': form.errors}
