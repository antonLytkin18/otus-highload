from wtforms import Form, StringField, validators, IntegerField


class ChatForm(Form):
    user_id = IntegerField(validators=[validators.required()])


class ChatMessageForm(Form):
    message = StringField(validators=[validators.required()])
