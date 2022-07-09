#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" HERMES application entry point. """

from hermes.core import config
from hermes.core import logger, server, plugins, storage


class App:
    """ The application main class. """

    _server = None
    _args = None

    def __init__(self):
        """ Instantiates the application. """
        print('== Loading HERMES ==')
        logger.init()
        plugins.init()
        storage.init()
        config.init()
        server.init()

    @classmethod
    def start(cls):
        """ Bootstraps the application. """
        logger.info('== Starting HERMES ==')
        server.start()

        # @todo remove once tests are finished.
        # while True:
        # command_name = input('Get a command?\n')
        # command = CommandFactory().get_by_name(command_name)
        # if command is None:
        #     logger.error(f'Command {command_name} do not exists.', command_name)
        #     continue
        #
        # BOARDS[1].send_command(command.code, 1, 180)
        # print(f'{str(command)} => DONE')
        # time.sleep(1)
        # print('PING')

    @classmethod
    def close(cls):
        """ Closes the application. """
        logger.info('== Stopping HERMES ==')
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
