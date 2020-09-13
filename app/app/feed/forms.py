from wtforms import Form, StringField, validators


class FeedPostForm(Form):
    message = StringField(validators=[validators.required()])
