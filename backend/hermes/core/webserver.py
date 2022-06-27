"""
This webserver is responsible for :
    - expose (mandatory) the socket.io API to help remote UIs to send commands (@see `frontend` directory)
    - expose (optional)  the http server to serve a default UI (@see `frontend` directory)
"""

from threading import Thread

from flask import Flask, jsonify, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from hermes import __version__
from hermes.core import config

# @todo Move this to a configurable
_PORT = 9999


class _WebServerThread(Thread):
    """ Custom thread class to the webserver in the background. """

    def __init__(self):
        """ Initializes the webserver (socker + http). """

        Thread.__init__(self)
        self.daemon = True

        # ----------------------------------------
        # Web  server route definition
        # ----------------------------------------
        self._server = Flask(__name__)
        CORS(self._server)

        @self._server.route("/heartbeat")
        def heartbeat():
            return jsonify({
                'status': 'healthy',
                'version': __version__
            })

        # ----------------------------------------
        # SockerIO server route definition
        # ----------------------------------------
        self._socketio = SocketIO(self._server, cors_allowed_origins='*')

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

        # ----------------------------------------
        # WebGUI optional definition
        # ----------------------------------------
        if config.CONFIG['webGUI']:
            @self._server.route('/', defaults={'path': ''})
            @self._server.route('/<string:path>')
            @self._server.route('/<path:path>')
            def index(path):
                # Defaults all what is not a static file to index.html:
                # ie defer the handling to vue (@see `frontend` folder).
                if '.' not in path:
                    path = 'index.html'
                return send_file("../../frontend/dist/" + path)

    def run(self):
        self._socketio.run(self._server, host="0.0.0.0", port=_PORT, debug=True, use_reloader=False)

    def close(self):
        self._socketio.stop()


WEBSERVER: _WebServerThread


def init():
    """ Starts the webserver. """
    print(' > Loading webserver')
    # pylint: disable-next=global-statement
    global WEBSERVER
    WEBSERVER = _WebServerThread()
    WEBSERVER.start()


def close():
    print(' > Close webserver')
    if WEBSERVER.is_alive():
        WEBSERVER.close()
        WEBSERVER.join()
