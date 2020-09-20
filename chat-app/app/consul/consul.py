import socket

from app.consul import consul


def init_consul(app):
    consul.init_app(app)
    chat_app_host = app.config.get('CHAT_APP_HOST')
    chat_app_port = app.config.get('CHAT_APP_PORT')
    chat_app_url = app.config.get('CHAT_APP_URL')

    consul.register_service(
        service_id=socket.gethostname(),
        name='chat-app',
        address=chat_app_url,
        interval='10s',
        httpcheck=f'http://{chat_app_host}:{chat_app_port}/healthcheck'
    )
