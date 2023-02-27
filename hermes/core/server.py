"""
This webserver is responsible for :
    - expose (mandatory) the socket.io API to help remote UIs to send commands (@see `https://github.com/dclause/hermes_vuejs` fro an example)
    - expose (optional)  the server to serve a default GUI (@see `gui` directory)
"""
import asyncio
import webbrowser
from threading import Thread

import uvicorn
from fastapi import FastAPI
from uvicorn import Server
from uvicorn.supervisors import ChangeReload, Multiprocess

from hermes import api, gui, __version__
from hermes.__main__ import App
from hermes.core import logger, cli


class _ServerThread(Thread):
    """ Custom thread class to the webserver in the background. """

    def __init__(self, instance: any, config: any):
        """ Initializes the webserver (socker + http). """
        Thread.__init__(self)

        self.config = uvicorn.Config(instance,
                                     factory=isinstance(instance, str),
                                     host=config['host'],
                                     port=config['port'],
                                     log_level='debug' if config['debug'] else 'warning',
                                     reload=config['dev'],
                                     reload_includes=['*.py', '*.css'] if config['dev'] else None
                                     )
        self.uvicorn_instance = None

    def run(self):

        # Hack into uvicorn to remove handled signals.
        # This allows to use uvicorn in threads, but requires to handle gracefully shutdown ourselves. Otherwise, the
        # auto-reload would have pending threads leaking from the application.
        # uvicorn.server.HANDLED_SIGNALS = []
        uvicorn.supervisors.basereload.HANDLED_SIGNALS = []

        # ****************************************************************************************
        # All the following is equivalent of calling  uvicorn.run() directly.
        # The only reason not to do so is to get an instance of the server running, so we can gracefully close it
        # in close() method.
        _server = Server(config=self.config)
        if self.config.should_reload:
            sock = self.config.bind_socket()
            self.uvicorn_instance = ChangeReload(self.config, target=_server.run, sockets=[sock])
        elif self.config.workers > 1:
            sock = self.config.bind_socket()
            self.uvicorn_instance = Multiprocess(self.config, target=_server.run, sockets=[sock])
        else:
            self.uvicorn_instance = _server
        self.uvicorn_instance.run()
        # ****************************************************************************************

    def close(self):
        """ Closes the socketIO connection. """
        if self.config.should_reload or self.config.workers > 1:
            self.uvicorn_instance.should_exit.set()
            self.uvicorn_instance.shutdown()
        else:
            # @todo when no reload is set: an error is triggered on close
            self.uvicorn_instance.should_exit = True
            self.uvicorn_instance.force_exit = True
            asyncio.run(self.uvicorn_instance.shutdown())


server = _ServerThread('hermes.core.server:factory', cli.args)


def factory() -> FastAPI:
    """
    Factory method for server.
    @see --factory option in uvicorn: https://www.uvicorn.org/#application-factories
    """
    app = FastAPI()

    @app.get("/version")
    def healthcheck():
        return {'status': 'healthy', 'version': __version__}

    @app.on_event('startup')
    def process():
        App()

    api.init(app)
    gui.init(app)
    return app


def start():
    """ Starts the servers. """
    config = cli.args
    auto_open = config.get('open')

    logger.info(f' > Start server {"(auto-open GUI)" if auto_open else ""}')

    # Auto open the browser.
    if auto_open:
        host = config.get('host')
        port = config.get('port')
        # @todo: certificate to use the GUI through https.
        webbrowser.open(f'http://{host if host != "0.0.0.0" else "127.0.0.1"}:{port}/')

    # Start the server.
    server.start()


def close():
    """ Stops the server. """
    logger.info(' > Shutdown the server')
    if server.is_alive():
        server.close()
        server.join()
