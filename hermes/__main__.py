#!/usr/bin/env python3

"""
HERMES application entry point.
@todo Remove all 'noqa D102' once:
    https://github.com/charliermarsh/ruff/issues/2413
    https://github.com/ott-jax/ott/pull/269.
"""
import webbrowser

from hermes.core import logger, plugins, server, storage
from hermes.core.config import settings


def main() -> None:
    """Bootstraps and run the application."""

    print('\033[96m == Loading HERMES == \033[0m')
    logger.init()
    plugins.init()
    storage.init()
    settings.init()
    server.init()

    try:

        logger.info('\033[96m == Starting HERMES == \033[0m')
        with server.server.run_in_thread():
            host = settings.get(['server', 'host'])
            port = settings.get(['server', 'port'])
            reload = settings.get(['server', 'reload'])
            ssl = settings.get(['server', 'ssl'])
            addr = f'http{"s" if ssl else ""}://{host}:{port}'
            logger.info(f' > Server running {"with autoreload" if reload else ""} on {addr} (Ctrl+C to quit)')

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


if __name__ == '__main__':
    main()

__ALL__: list[str] = []
