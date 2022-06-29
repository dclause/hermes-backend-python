#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" HERMES application entry point. """

from hermes.core import boards, logger, server, plugins, storage
from hermes.core import config
from hermes.core.boards.arduino import ArduinoBoard
from hermes.core.devices.led import LedDevice
from hermes.core.storage import StorageType


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
        print('== Starting HERMES ==')
        logger.info('== Starting HERMES ==')
        server.start()

        # while True:
        # command_name = input('Get a command?\n')
        # command = CommandFactory().get_by_name(command_name)
        # if command is None:
        #     logger.error('Command %s do not exists.', command_name)
        #     continue
        #
        # BOARDS[1].send_command(command.code, 1, 180)
        # print(f'{str(command)} => DONE')
        # time.sleep(1)
        # print('PING')

    @classmethod
    def close(cls):
        """ Closes the application. """
        print('== Stopping HERMES ==')
        logger.info('== Stopping HERMES ==')
        server.close()


if __name__ == "__main__":

    # leds =  [LedDevice('myled1', 13, False), LedDevice('myled2', 14, False), LedDevice('myled3', 15, False)]
    # with open('output_file.txt', 'w') as file:
    #     yaml.dump_all(leds, file, Dumper=DataDumper)

    hermes = App()
    try:
        hermes.start()

        # @todo: logger.info should print on screen and avoid duplicate here.
        print('== Running HERMES ==')
        logger.info('== Running HERMES ==')

        # CommandFactory()

        # board1 = ArduinoBoard('Board A', 'COM3')
        # boards = [board1, ArduinoBoard('Board B', 'COM4')]
        # devices = [
        #     LedDevice('myled1', board1, 13, False),
        #     LedDevice('myled2', board1, 14, False),
        #     LedDevice('myled3', boards[1], 15, False)
        # ]
        #
        # with open('output_file.yaml', 'w') as file:
        #     storage.storage.dump_all(devices, file)
        #
        # with open('output_file.yaml', 'r') as file:
        #     docs = storage.storage.load_all(file)
        #     for doc in docs:
        #         print(doc)
        #         print('associated board', doc.board)

        # obj: dict[str: str] = {
        #     'server': {
        #         'host': '0.0.0.0',
        #         'port': 4000,
        #         'debug': True
        #     },
        #     'socket': {
        #         'host': '0.0.0.0',
        #         'port': 9999,
        #     },
        #     'web': {
        #         'host': '0.0.0.0',
        #         'port': 4000,
        #     }
        # }
        # storage.write(StorageType.GLOBAL, obj)

        while True:
            pass

    except KeyboardInterrupt:
        hermes.close()
