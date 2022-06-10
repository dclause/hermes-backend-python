from threading import Thread

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit

_data = 'foo'
_host_name = "0.0.0.0"
_port = 9999
_app = Flask(__name__)
_app.config['SECRET_KEY'] = 'secret!'
CORS(_app)

class SocketThread1(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        while True:
            pass
            # print('A')

class SocketThread2(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        while True:
            pass
            # print('B')


class SocketThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self._socketio = SocketIO(_app, cors_allowed_origins='*')

        @self._socketio.on('mutation')
        def mutation(message):
            print('## received', message)
            emit('patch', message, broadcast=True)

        @self._socketio.on('connect')
        def connect(payload):
            print('## client connected', payload)

        @self._socketio.on('disconnect')
        def disconnect(payload):
            print('## client disconnect', payload)

        self.start()

    def run(self):
        self._socketio.run(_app, host=_host_name, port=_port, debug=True, use_reloader=False)

    # socketio.start_background_task(start_server)
