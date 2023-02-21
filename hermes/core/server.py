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
from uvicorn.supervisors import ChangeReload

from hermes.core import logger
from hermes.core.config import CONFIG
from hermes.ui import frontend


class _ServerThread(Thread):
    """ Custom thread class to the webserver in the background. """

    def __init__(self):
        """ Initializes the webserver (socker + http). """

        Thread.__init__(self)
        self.api = FastAPI()
        self.ui = FastAPI()

        # ----------------------------------------
        # SockerIO server route definition
        # ----------------------------------------
        # @todo socket API.

    def run(self):
        log_level = 'debug' if CONFIG.get('global')['debug'] else 'info'
        # uvicorn.server.HANDLED_SIGNALS = []
        uvicorn.supervisors.basereload.HANDLED_SIGNALS = []
        uvicorn.run('hermes.core.server:init',
                    host=CONFIG.get('global')['ui']['host'],
                    port=CONFIG.get('global')['ui']['port'],
                    log_level=log_level,
                    reload=True,
                    reload_dirs=['hermes'],
                    reload_includes=['*.py']
                    )  # @todo allow reload=True
        # config = uvicorn.Config('hermes.core.server:SERVER.ui',
        #                         host=CONFIG.get('global')['ui']['host'],
        #                         port=CONFIG.get('global')['ui']['port'],
        #                         log_level=log_level,
        #                         reload=True,
        #                         reload_dirs=['hermes'],
        #                         reload_includes=['*.py']
        #                         )  # @todo allow reload=True
        # server = uvicorn.Server(config=config)
        # sock = config.bind_socket()
        # ChangeReload(config, target=server.run, sockets=[sock]).run()

    def close(self):
        """ Closes the socketIO connection. """
        # @todo


SERVER = _ServerThread()

def init():
    """ Starts the webserver. """
    logger.info(' > Loading server')

    frontend.init(SERVER.ui)

    return SERVER.ui
    # if CONFIG.get('global')['api']['enabled']:
    #     api.init(_server.app)


def start():
    """ Starts the webserver. """
    start_api = CONFIG.get('global')['api']['enabled']
    start_ui = CONFIG.get('global')['ui']['enabled']
    auto_open = start_ui and CONFIG.get('global')['ui']['open']

    logger.info(f' > Start server  '
                f'{"-with API-" if start_api else ""} '
                f'{"-with UI" if start_ui else ""}'
                f'{" (auto-open)-" if auto_open else "-"}')

    # Auto open the browser.
    if auto_open:
        host = CONFIG.get('global')['ui']['host']
        port = CONFIG.get('global')['ui']['port']
        webbrowser.open(f'http://{host if host != "0.0.0.0" else "127.0.0.1"}:{port}/')

    if start_api or start_ui:
        SERVER.start()


def close():
    """ Stops the webserver. """
    logger.info(' > Close webserver')
    if SERVER.is_alive():
        SERVER.close()
        SERVER.join()
