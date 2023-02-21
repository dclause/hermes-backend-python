"""
This webserver is responsible for :
    - expose (mandatory) the socket.io API to help remote UIs to send commands (@see `frontend` directory)
    - expose (optional)  the http server to serve a default UI (@see `frontend` directory)

@todo convert this all from flask to fastAPI.
@todo remove flask dependency all together.
"""
import webbrowser
from threading import Thread

import uvicorn
from fastapi import FastAPI

from hermes import __version__
from hermes.core import logger
from hermes.core.config import CONFIG
from hermes.ui import frontend


class _ServerThread(Thread):
    """ Custom thread class to the webserver in the background. """

    def __init__(self):
        """ Initializes the webserver (socker + http). """

        Thread.__init__(self)
        self.app = FastAPI()

        # ----------------------------------------
        # Web  server route definition
        # ----------------------------------------
        # @todo CORS for the server ?

        @self.app.get("/healthcheck")
        @self.app.get("/healthcheck")
        def healthcheck():
            return {
                'status': 'healthy',
                'version': __version__
            }

        # ----------------------------------------
        # SockerIO server route definition
        # ----------------------------------------
        # @todo socket API.

    def run(self):
        host = CONFIG.get('global')['server']['host']
        port = CONFIG.get('global')['server']['port']
        debug = CONFIG.get('global')['debug']
        log_level = 'debug' if debug else 'error'
        uvicorn.run(self.app, host=host, port=port, log_level=log_level)  # @todo allow reload=True

    def close(self):
        """ Closes the socketIO connection. """
        # @todo


_server = _ServerThread()


def init():
    """ Starts the webserver. """
    logger.info(' > Loading server')
    if CONFIG.get('global')['ui']['enabled']:
        frontend.init(_server.app)
    # if CONFIG.get('global')['api']['enabled']:
    #     api.init(_server.app)


def start():
    """ Starts the webserver. """
    start_api = CONFIG.get('global')['api']['enabled']
    start_ui = CONFIG.get('global')['ui']['enabled']
    auto_open = start_ui and CONFIG.get('global')['ui']['open']

    logger.info(
        f' > Start server {"-with api-" if start_api else ""} {"-with gui-" if start_ui else ""} {"(auto-open)" if auto_open else ""}')

    if auto_open:
        host = CONFIG.get('global')['server']['host']
        port = CONFIG.get('global')['server']['port']
        webbrowser.open(f'http://{host if host != "0.0.0.0" else "127.0.0.1"}:{port}/')

    if start_api or start_ui:
        _server.start()


def close():
    """ Stops the webserver. """
    logger.info(' > Close webserver')
    if _server.is_alive():
        _server.close()
        _server.join()
