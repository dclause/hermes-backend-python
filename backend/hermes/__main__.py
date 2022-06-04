#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" HERMES application entry point. """

from flask import Flask, jsonify
from flask_cors import CORS

from hermes import __version__
from hermes.core import boards, logger, config
from hermes.core.boards import BOARDS
from hermes.core.config import CONFIG


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

        print('All boards')
        print(BOARDS)

    @classmethod
    def start(cls):
        """ Bootstraps the application. """
        print('== Starting HERMES ==')
        logger.info('== Starting HERMES ==')
        # self._start_gui()

        while True:
            command_name = input('Get a command?\n')
            command = command.CommandFactory().get_by_name(command_name)
            if command is None:
                logger.error('Command %s do not exists.', command_name)
                continue
            BOARDS[1].send_command(command.code)
            print(f'{str(command)} => DONE')

    @classmethod
    def close(cls):
        """ Closes the application. """
        print('== Stopping HERMES ==')
        print('> Close boards connection')
        for _, board in BOARDS.items():
            board.close()

    def _start_gui(self, configuration=None):
        """ Starts the flask server to serve the UI. """
        self._server = Flask(__name__)

        # See http://flask.pocoo.org/docs/latest/config/
        self._server.config.update(dict(DEBUG=True))
        self._server.config.update(configuration or {})

        # Setup cors headers to allow all domains
        # https://flask-cors.readthedocs.io/en/latest/
        CORS(self._server)

        # Definition of the routes. Put them into their own file. See also
        # Flask Blueprints: http://flask.pocoo.org/docs/latest/blueprints
        @self._server.route("/")
        def hello_world():
            logger.info("/")
            return "Hello World"

        @self._server.route("/ping")
        def ping():
            logger.info("/ping")
            return jsonify({"echo": __version__})

        self._server.run(host="127.0.0.1", port=CONFIG['port'])


if __name__ == "__main__":
    hermes = App()
    try:
        hermes.start()
    except KeyboardInterrupt:
        hermes.close()
