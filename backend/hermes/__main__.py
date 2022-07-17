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
        for (_, board) in config.BOARDS.items():
            board.open()

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
        for (_, board) in config.BOARDS.items():
            board.close()
        server.close()


# def save():
#     hermes = App()
#     data = {
#                'id': 1,
#                'type': 'LED',
#                'name': 'Demo LED',
#                'board': 1,
#                'controls': [
#                    BooleanAction(),
#                    OnOffCommand(),
#                ],
#            },
#
#     _storage = ruamel.yaml.YAML(typ='safe')
#     _storage.sort_base_mapping_type_on_output = False
#     with open('test.yml', 'w', encoding='utf-8') as file:
#         _storage.dump_all(data, file)
#
#     sys.exit()


if __name__ == "__main__":
    # save()
    hermes = App()
    try:
        hermes.start()
        logger.info('== Running HERMES ==')

        while True:
            pass

    except KeyboardInterrupt:
        hermes.close()
