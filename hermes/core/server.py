"""
The server section is responsible for :
    - serves a default GUI (@see `gui` directory)
    - exposes the socket.io API to help remote UIs to send commands
        @see `https://github.com/dclause/hermes_vuejs` for an example.
"""
import contextlib
import threading
import time
from socket import socket
from typing import List

import uvicorn
from fastapi import FastAPI
from uvicorn import Config
from uvicorn.supervisors import ChangeReload

from hermes import __version__, gui
from hermes.core import api, logger, plugins, storage
from hermes.core.config import settings


class _ChangeReloadServer(ChangeReload):
    """ Overrides the default uvicorn server to run in a separated thread context. """

    def __init__(
            self,
            _server: uvicorn.Server,
            _config: Config,
            _sockets: List[socket],
    ) -> None:
        super().__init__(_config, _server.run, _sockets)
        uvicorn.supervisors.basereload.HANDLED_SIGNALS = []
        self._server = _server
        self.started = False

    def run(self):
        self.started = True
        super().run()

    @contextlib.contextmanager
    def run_in_thread(self):
        """ To be called instead of uvicorn.run() to run the server in a dedicated thread. """
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self._server.should_exit = True
            self.should_exit.set()
            thread.join()


class _Server(uvicorn.Server):
    """ Overrides the default uvicorn server to run in a separated thread context. """

    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self, sockets=None):
        """ To be called instead of uvicorn.run() to run the server in a dedicated thread. """
        thread = threading.Thread(target=self.run, args=(sockets,))
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()


# pylint: disable-next=invalid-name
server = None


def init():
    """ Initializes the server. """
    # pylint: disable-next=invalid-name,global-statement
    global server
    config = Config(
        'hermes.core.server:reload_factory' if settings.get(['server', 'reload']) else 'hermes.core.server:factory',
        factory=True,
        host=settings.get(['server', 'host']),
        port=settings.get(['server', 'port']),
        log_level='warning',
        reload=settings.get(['server', 'reload']),
        reload_includes=['*.py', '*.css'] if settings.get(['server', 'reload']) else None)

    server = _Server(config=config)
    if config.should_reload:
        sock = config.bind_socket()
        server = _ChangeReloadServer(_server=server, _config=config, _sockets=[sock])


def factory() -> FastAPI:
    """
    Factory method for server.
    @see --factory option in uvicorn: https://www.uvicorn.org/#application-factories.
    """
    app = FastAPI()

    @app.get("/version")
    def healthcheck():
        return {'status': 'healthy', 'version': __version__}

    api.init(app)
    gui.init(app)
    return app


def reload_factory() -> FastAPI:
    """
    Reloadable factory for server.
    Uses the standard factory but also reuses the hermes init() application bootstrap.
    @see factory().
    """
    logger.init()
    plugins.init()
    storage.init()
    settings.init()
    return factory()
