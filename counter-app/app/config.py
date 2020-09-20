import os


class Config:
    DEBUG = os.environ.get('DEBUG')
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    WTF_CSRF_CHECK_DEFAULT = os.environ.get('WTF_CSRF_CHECK_DEFAULT')

    REDIS_CACHE_HOST = os.environ.get('REDIS_CACHE_HOST')
