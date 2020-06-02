from wtforms import IntegerField, StringField, PasswordField, Form, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import EqualTo


class RegistrationForm(Form):
    name = StringField(validators=[validators.required()])
    last_name = StringField(validators=[validators.required()])
    email = StringField(validators=[validators.email()])
    password = PasswordField('Password', validators=[validators.required(), EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password')
    age = IntegerField(validators=[validators.required()])
    interests = StringField()
    city = StringField(validators=[validators.required()])


class AuthForm(Form):
    email = EmailField(
        'Enter e-mail',
        validators=[validators.email()],
        render_kw={'placeholder': 'E-mail'}
    )
    password = PasswordField(
        'Enter password',
        validators=[validators.required()],
        render_kw={'placeholder': 'Password'}
    )
