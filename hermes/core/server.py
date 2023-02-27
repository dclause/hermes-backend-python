"""
The server section is responsible for :
    - expose the socket.io API to help remote UIs to send commands (@see `https://github.com/dclause/hermes_vuejs` for an example)
    - serve a default GUI (@see `gui` directory)
"""
import contextlib
import threading
import time

import uvicorn
from fastapi import FastAPI
from uvicorn import Config

from hermes import api, gui, __version__
from hermes.core import cli


class _Server(uvicorn.Server):
    """ Overrides the default uvicorn server to run in a separated thread context. """
    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()


_cli_args = cli.args
_config = Config("hermes.core.server:factory",
                 factory=True,
                 host=_cli_args['host'],
                 port=_cli_args['port'],
                 log_level='debug' if _cli_args['debug'] else 'warning',
                 reload=_cli_args['dev'],
                 reload_includes=['*.py', '*.css'] if _cli_args['dev'] else None)
server = _Server(config=_config)


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
