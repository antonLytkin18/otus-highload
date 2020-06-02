import json


def tojson_escaped(obj):
    return json.dumps(obj)


def form_tojson(form):
    data = {field.name: {
        'id': field.id,
        'label': field.label.text,
        'type' : field.widget.input_type,
        'required': field.flags.required,
        'placeholder': field.render_kw.get('placeholder') if field.render_kw else field.label.text,
    } for field in form}

    return json.dumps(data)
