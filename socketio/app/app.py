import os

from flask import Flask
from flask_socketio import SocketIO, join_room
from gevent.monkey import patch_all

app = Flask(__name__)
socketio = SocketIO(app, logger=True, cors_allowed_origins='*', message_queue=os.environ.get('SOCKETIO_BROKER_URL'))

patch_all()


@socketio.on('join')
def on_join(data):
    join_room(data['room'])


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)
