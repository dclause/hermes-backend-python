"""
This webserver is responsible for :
    - expose (mandatory) the socket.io API to help remote UIs to send commands (@see `frontend` directory)
    - expose (optional)  the http server to serve a default UI (@see `frontend` directory)

@todo convert this all from flask to fastAPI.
@todo remove flask dependency all together.
"""
import os
from threading import Thread
from typing import Any

from flask import Flask, jsonify, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from hermes import __version__
from hermes.core import logger
from hermes.core.config import CONFIG
from hermes.devices import AbstractDevice
from hermes.core.helpers import ROOT_DIR

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

        @self._socketio.on('connect')
        def connect(payload):
            logger.info(f'## socketIO client connected: {payload}')
            handshake()

        @self._socketio.on('disconnect')
        def disconnect():
            logger.info('## socketIO client disconnected')

        @self._socketio.on('ping')
        def ping():
            """
            Answer to a ping by a pong.
            This can be used by the clients to check the latency of a ping/pong message exchange with this server.
            """
            emit('pong')

        @self._socketio.on('handshake')
        def handshake():
            """
            Pushes all current config to the client.
            """
            emit('handshake', (
                CONFIG.get('global'),
                CONFIG.get('profile'),
                {key: board.serialize(recursive=True) for key, board in CONFIG.get('boards').items()},
                CONFIG.get('groups'),
            ))

        @self._socketio.on('action')
        def mutation(board_id: int, command_id: int, value: Any):
            logger.debug(f'## socketIO received "Mutation" with parameter: {board_id} {command_id} {value}')
            try:
                device: AbstractDevice = CONFIG.get('boards')[board_id].actions[command_id]
                device.set_value(board_id, value)
                CONFIG.get('boards')[board_id].actions[command_id].state = value
            except Exception as exception:
                logger.error(f'Mutation error: command could not be sent because: "{exception}".')
            emit('patch', (board_id, CONFIG.get('boards')[board_id].serialize(recursive=True)), broadcast=True)

        # ----------------------------------------
        # WebGUI optional definition
        # ----------------------------------------.
        if CONFIG.get('global')['web']['enabled']:

            @self._server.route('/', defaults={'path': ''})
            @self._server.route('/<string:path>')
            @self._server.route('/<path:path>')
            def index(path):
                # Defaults all what is not a static file to index.html:
                # ie defer the handling to vue (@see `frontend` folder).
                if '.' not in path:
                    path = 'index.html'
                return send_file(os.path.join(ROOT_DIR, '..', '..', 'frontend', 'dist', path))

    def run(self):
        self._socketio.run(
            self._server,
            host=CONFIG.get('global')['server']['host'],
            port=CONFIG.get('global')['server']['port'],
            debug=CONFIG.get('global')['server']['debug'],
            use_reloader=False
        )

    def close(self):
        """ Closes the socketIO connection. """
        self._socketio.stop()


_WEBSERVER: _WebServerThread


def init():
    """ Starts the webserver. """
    logger.info(' > Loading webserver')


def start():
    """ Starts the webserver. """
    logger.info(' > Start webserver')
    # pylint: disable-next=global-statement
    global _WEBSERVER
    _WEBSERVER = _WebServerThread()
    _WEBSERVER.start()


def close():
    """ Stops the webserver. """
    logger.info(' > Close webserver')
    if _WEBSERVER.is_alive():
        _WEBSERVER.close()
        _WEBSERVER.join()
