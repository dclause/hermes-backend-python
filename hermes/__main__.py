#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" HERMES application entry point. """
import webbrowser

from hermes.core import logger, plugins, storage, server
from hermes.core.config import settings


def main():
    """ Main program entry point. """

    print('\033[96m == Loading HERMES == \033[0m')
    logger.init()
    plugins.init()
    storage.init()
    settings.init()
    server.init()

    try:

        logger.info('\033[96m == Starting HERMES == \033[0m')
        with server.server.run_in_thread():

            # @todo: certificate to use the GUI through https.
            host = settings.get(['server', 'host'])
            port = settings.get(['server', 'port'])
            addr = f'http://{host if host != "0.0.0.0" else "127.0.0.1"}:{port}'
            logger.info(f' > Server running on {addr} (Ctrl+C to quit)')

            # Auto open the browser.
            if settings.get(['server', 'open']):
                webbrowser.open(addr)

            # Start boards.
            for (_, board) in settings.get('boards').items():
                board.open()

            # Main loop.
            while True:
                pass

    except KeyboardInterrupt:
        logger.info('\033[96m == Stopping HERMES == \033[0m')
        for (_, board) in settings.get('boards').items():
            board.close()


if __name__ == "__main__":
    main()
