import os


class Config:
    DEBUG = os.environ.get('DEBUG')
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    WTF_CSRF_CHECK_DEFAULT = os.environ.get('WTF_CSRF_CHECK_DEFAULT')

    MYSQL_HOST = os.environ.get('CHAT_APP_MYSQL_HOST')
    MYSQL_PORT = int(os.environ.get('CHAT_SERVICE_MYSQL_PORT', 3306))
    MYSQL_USER = os.environ.get('CHAT_APP_MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('CHAT_APP_MYSQL_PASSWORD')
    MYSQL_DB = os.environ.get('CHAT_APP_MYSQL_DB')

    MAIN_BROKER_URL = os.environ.get('MAIN_BROKER_URL')

