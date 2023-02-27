#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" HERMES application entry point. """

from hermes.core.config import CONFIG
from hermes.core import logger, server, plugins, storage
from hermes.core.struct import MetaSingleton


class App(metaclass=MetaSingleton):
    """ The application main class. """

    def __init__(self, *args):
        """ Instantiates the application. """
        print('== Loading HERMES ==')
        logger.init()
        plugins.init()
        storage.init()
        CONFIG.init()

    @classmethod
    def start(cls):
        """ Bootstraps the application. """
        logger.info('== Starting HERMES ==')
        for (_, board) in CONFIG.get('boards').items():
            board.open()

    @classmethod
    def close(cls):
        """ Closes the application. """
        logger.info('== Stopping HERMES ==')
        for (_, board) in CONFIG.get('boards').items():
            board.close()
        server.close()
        logger.info('== Stopped HERMES ==')


if __name__ == "__main__":
    server.start()
    hermes = App()
    try:
        logger.info('== Running HERMES ==')
        hermes.start()

        while True:
            pass
    except KeyboardInterrupt:
        hermes.close()
