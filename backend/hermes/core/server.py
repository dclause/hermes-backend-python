"""
This webserver is responsible for :
    - expose (mandatory) the socket.io API to help remote UIs to send commands (@see `frontend` directory)
    - expose (optional)  the http server to serve a default UI (@see `frontend` directory)
"""
import os
from threading import Thread
from typing import Any

from flask import Flask, jsonify, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from hermes import __version__
from hermes.core import config, logger
from hermes.core.commands import CommandFactory
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
            # self._socketio.emit('handshake', (
            #     config.GLOBAL,
            #     config.PROFILE,
            #     storage.dump(config.BOARDS),
            #     storage.dump(config.DEVICES)
            # ))
            emit('handshake', (
                config.GLOBAL,
                config.PROFILE,
                {key: board.serialize() for key, board in config.BOARDS.items()},
                {key: device.serialize() for key, device in config.DEVICES.items()}
            ))

        @self._socketio.on('mutation')
        def mutation(message: dict[str, Any]):
            logger.debug('## received %s', message)
            emit('patch', message, broadcast=True)
            config.update(message)
            command_name = list(message.keys())[0]
            command = CommandFactory().get_by_name(command_name)
            if command is None:
                logger.error('Command %s do not exists.', command_name)
            config.BOARDS[1].send_command(command.code, message[command_name])

        # ----------------------------------------
        # WebGUI optional definition
        # ----------------------------------------
        if config.GLOBAL['web']['enabled']:
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
            host=config.GLOBAL['server']['host'],
            port=config.GLOBAL['server']['port'],
            debug=config.GLOBAL['server']['debug'],
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
