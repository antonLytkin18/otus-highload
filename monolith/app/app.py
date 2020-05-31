from flask import Flask
from flask_injector import FlaskInjector
# from app import application
# from app import create_app
# from app.dependencies import configure

if __name__ == '__main__':
    # app = create_app()
    app = Flask(__name__)
    # FlaskInjector(app=app, modules=[configure])
    FlaskInjector(app=app, modules=[])
    app.run(host='0.0.0.0', debug=True)
