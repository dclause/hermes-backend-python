"""
The server section is responsible for :
    - serves a default GUI (@see `gui` directory)
    - exposes the socket.io API to help remote UIs to send commands
        @see `https://github.com/dclause/hermes_vuejs` for an example
"""
import contextlib
import threading
import time

import uvicorn
from fastapi import FastAPI
from uvicorn import Config

from hermes import api, gui, __version__
from hermes.core.config import settings


class _Server(uvicorn.Server):
    """ Overrides the default uvicorn server to run in a separated thread context. """

    def install_signal_handlers(self):
        pass

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
            self.should_exit = True
            thread.join()


server = None  # pylint: disable=invalid-name


def init():
    """ Initializes the server """
    global server  # pylint: disable=invalid-name,global-statement
    config = Config("hermes.core.server:factory",
                    factory=True,
                    host=settings.get(['server', 'host']),
                    port=settings.get(['server', 'port']),
                    log_level='warning',
                    reload=settings.get(['server', 'reload']),
                    reload_includes=['*.py', '*.css'] if settings.get(['server', 'reload']) else None)
    server = _Server(config=config)


def factory() -> FastAPI:
    """
    Factory method for server.
    @see --factory option in uvicorn: https://www.uvicorn.org/#application-factories
    """
    app = FastAPI()

    @app.get("/version")
    def healthcheck():
        return {'status': 'healthy', 'version': __version__}

    api.init(app)
    gui.init(app)
    return app
