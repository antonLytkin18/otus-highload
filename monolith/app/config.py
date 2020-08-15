import os


class Config:
    DEBUG = os.environ.get('DEBUG')
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    WTF_CSRF_CHECK_DEFAULT = os.environ.get('WTF_CSRF_CHECK_DEFAULT')

    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_DB = os.environ.get('MYSQL_DB')

    SLAVE_MYSQL_HOST = os.environ.get('SLAVE_MYSQL_HOST')
    SLAVE_MYSQL_PORT = int(os.environ.get('SLAVE_MYSQL_PORT', 3306))
    SLAVE_MYSQL_USER = os.environ.get('SLAVE_MYSQL_USER')
    SLAVE_MYSQL_PASSWORD = os.environ.get('SLAVE_MYSQL_PASSWORD')
    SLAVE_MYSQL_DB = os.environ.get('SLAVE_MYSQL_DB')

    CHAT_MYSQL_HOST = os.environ.get('CHAT_MYSQL_HOST')
    CHAT_MYSQL_PORT = int(os.environ.get('CHAT_MYSQL_PORT', 3306))
    CHAT_MYSQL_USER = os.environ.get('CHAT_MYSQL_USER')
    CHAT_MYSQL_PASSWORD = os.environ.get('CHAT_MYSQL_PASSWORD')
    CHAT_MYSQL_DB = os.environ.get('CHAT_MYSQL_DB')

    TARANTOOL_HOST = os.environ.get('TARANTOOL_HOST')
    TARANTOOL_PORT = int(os.environ.get('TARANTOOL_PORT', 3301))