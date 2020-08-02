from wtforms import Form, StringField, validators


class ChatMessageForm(Form):
    message = StringField(validators=[validators.required()])
