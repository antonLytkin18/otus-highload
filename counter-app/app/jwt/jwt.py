from flask_jwt import JWT

jwt = JWT(
    authentication_handler=lambda *args, **kwargs: None,
    identity_handler=lambda payload: payload['identity']
)
