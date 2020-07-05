from wtforms import Form, StringField


class FilterForm(Form):
    last_name_like = StringField('Last Name', render_kw={'placeholder': None})
    name_like = StringField('Name', render_kw={'placeholder': None})
