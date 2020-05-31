from wtforms import IntegerField, StringField, PasswordField, Form, validators
from wtforms.validators import EqualTo

class RegistrationForm(Form):
    name = StringField(validators=[validators.required()])
    lastName = StringField(validators=[validators.required()])
    email = StringField(validators=[validators.email()])
    password = PasswordField('Password', validators=[validators.required(), EqualTo('confirmPassword')])
    confirmPassword = PasswordField('Confirm Password')
    age = IntegerField(validators=[validators.required()])
    city = StringField(validators=[validators.required()])


class AuthForm(Form):
    email = StringField(validators=[validators.email()])
    password = PasswordField('Password', validators=[validators.required()])
