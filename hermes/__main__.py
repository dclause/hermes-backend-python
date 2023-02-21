#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" HERMES application entry point. """
from hermes.core import logger, server, plugins, storage
from hermes.core.config import CONFIG


class App:
    """ The application main class. """

    def __init__(self):
        """ Instantiates the application. """
        print('== Loading HERMES ==')
        logger.init()
        plugins.init()
        storage.init()
        CONFIG.init()
        server.init()

    @classmethod
    def start(cls):
        """ Bootstraps the application. """
        logger.info('== Starting HERMES ==')
        server.start()
        for (_, board) in CONFIG.get('boards').items():
            board.open()

    @classmethod
    def close(cls):
        """ Closes the application. """
        logger.info('== Stopping HERMES ==')
        for (_, board) in CONFIG.get('boards').items():
            board.close()
        server.close()


if __name__ == "__main__":
    hermes = App()
    try:
        hermes.start()
        logger.info('== Running HERMES ==')

        while True:
            pass
    except KeyboardInterrupt:
        hermes.close()
