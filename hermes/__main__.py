#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" HERMES application entry point. """
import webbrowser

from hermes.core import logger, plugins, storage, cli
from hermes.core.config import CONFIG
from hermes.core.server import server


def main():
    """ Main program entry point. """

    print('== Loading HERMES ==')
    logger.init()
    plugins.init()
    storage.init()
    CONFIG.init()
    config = cli.args  # rework
    auto_open = config.get('open')

    try:

        logger.info('== Starting HERMES ==')
        with server.run_in_thread():

            # Auto open the browser.
            logger.info(f' > Start server {"(auto-open GUI)" if auto_open else ""}')
            if auto_open:
                host = config.get('host')
                port = config.get('port')
                # @todo: certificate to use the GUI through https.
                webbrowser.open(f'http://{host if host != "0.0.0.0" else "127.0.0.1"}:{port}/')

            # Start boards.
            for (_, board) in CONFIG.get('boards').items():
                board.open()

            # Main loop.
            while True:
                pass

    except KeyboardInterrupt:
        logger.info('== Stopping HERMES ==')
        for (_, board) in CONFIG.get('boards').items():
            board.close()


if __name__ == "__main__":
    main()
