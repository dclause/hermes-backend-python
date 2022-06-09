import threading

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit

_data = 'foo'
_host_name = "0.0.0.0"
_port = 4444
_app = Flask(__name__)
_app.config['SECRET_KEY'] = 'secret!'
_app.debug = False
_app.use_reloader = False
CORS(_app)

def init():
    socketio = SocketIO(_app, cors_allowed_origins='*', debug=False, use_reloader=False)

    @socketio.on('mutation')
    def mutation(message):
        print('## received', message)
        emit('my response', {'data': 'got it!'})

    def start_server():
        print('starting map server')
        socketio.run(_app, port=8000, debug=False, use_reloader=False)

    socketio.start_background_task(start_server)
