#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" HERMES application entry point. """
import threading
from multiprocessing import Process, Value

from flask import Flask, jsonify, send_file
from flask_cors import CORS

from hermes import __version__
from hermes.core import boards, logger
from hermes.core import config
from hermes.core.boards import BOARDS
from hermes.core.command import CommandFactory


class App:
    """ The application main class. """

    _server = None
    _args = None

    def __init__(self):
        """ Instantiates the application. """
        print('== Loading HERMES ==')
        logger.init()
        config.init()
        boards.init()
        # socket.init()

        print('All boards')
        print(BOARDS)

    def start(self):
        """ Bootstraps the application. """
        print('== Starting HERMES ==')
        logger.info('== Starting HERMES ==')
        # self._start_gui()

        while True:
            command_name = input('Get a command?\n')
            command = CommandFactory().get_by_name(command_name)
            if command is None:
                logger.error('Command %s do not exists.', command_name)
                continue

            BOARDS[1].send_command(command.code, 1, 180)
            print(f'{str(command)} => DONE')

    @classmethod
    def close(cls):
        """ Closes the application. """
        print('== Stopping HERMES ==')
        print('> Close boards connection')
        for _, board in BOARDS.items():
            board.close()

    def start_gui(self, configuration=None):
        """ Starts the flask server to serve the UI. """
        self._server = Flask(__name__)

        # See http://flask.pocoo.org/docs/latest/config/
        self._server.config.update(dict(DEBUG=True))
        self._server.config.update(configuration or {})

        # Setup cors headers to allow all domains
        # https://flask-cors.readthedocs.io/en/latest/
        CORS(self._server)

        @self._server.route("/heartbeat")
        def heartbeat():
            return jsonify({
                'status': 'healthy',
                'version': __version__
            })

        @self._server.route('/', defaults={'path': ''})
        @self._server.route('/<string:path>')
        @self._server.route('/<path:path>')
        def index(path):
            # Defaults all what is not a static file to index.html:
            # ie defer the handling to vue (@see `frontend` folder).
            if '.' not in path:
                path = 'index.html'
            return send_file("../../frontend/dist/" + path)

        self._server.run(host="127.0.0.1", port=config.CONFIG['port'], debug=True, use_reloader=False)


if __name__ == "__main__":
    hermes = App()
    p = Process(target=hermes.start(), args=(Value('b', True),))
    try:
        p.start()
        hermes.start_gui()
    except KeyboardInterrupt:
        p.join()
        hermes.close()
