#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" HERMES application entry point. """
import yaml

from hermes.core import boards, logger, server, plugins
from hermes.core import config
from hermes.core.boards.arduino import ArduinoBoard
from hermes.core.commands import CommandFactory
from hermes.core.devices import DataDumper, DataLoader
from hermes.core.devices.led import LedDevice


class App:
    """ The application main class. """

    _server = None
    _args = None

    def __init__(self):
        """ Instantiates the application. """
        print('== Loading HERMES ==')
        logger.init()
        plugins.init()
        config.init()
        server.init()
        print('== Start HERMES ==')

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
        boards.close()
        server.close()


if __name__ == "__main__":

    # leds =  [LedDevice('myled1', 13, False), LedDevice('myled2', 14, False), LedDevice('myled3', 15, False)]
    # with open('output_file.txt', 'w') as file:
    #     yaml.dump_all(leds, file, Dumper=DataDumper)

    hermes = App()
    try:
        hermes.start()

        CommandFactory()

        board1 = ArduinoBoard('Board A', 'COM3')
        boards = [board1, ArduinoBoard('Board B', 'COM4')]
        devices = [
            LedDevice('myled1', board1, 13, False),
            LedDevice('myled2', board1, 14, False),
            LedDevice('myled3', boards[1], 15, False)
        ]
        with open('output_file.txt', 'w') as file:
            yaml.dump_all(devices, file, Dumper=DataDumper)

        with open('output_file.txt', 'r') as file:
            docs = yaml.load_all(file, Loader=DataLoader)
            for doc in docs:
                print(doc)
                print('associated board', doc.board)
        while True:
            pass

    except KeyboardInterrupt:
        hermes.close()
