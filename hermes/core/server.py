"""
This webserver is responsible for :
    - expose (mandatory) the socket.io API to help remote UIs to send commands (@see `https://github.com/dclause/hermes_vuejs` fro an example)
    - expose (optional)  the server to serve a default GUI (@see `gui` directory)
"""
import asyncio
import webbrowser
from threading import Thread

import mergedeep
import uvicorn
from uvicorn import Server
from uvicorn.supervisors import ChangeReload, Multiprocess

from hermes import api, ui
from hermes.core import logger
from hermes.core.config import CONFIG


class _ServerThread(Thread):
    """ Custom thread class to the webserver in the background. """

    def __init__(self, factory: any, config: any):
        """ Initializes the webserver (socker + http). """
        Thread.__init__(self)

        self.config = uvicorn.Config(factory,
                                     factory=isinstance(factory, str),
                                     host=config['host'],
                                     port=config['port'],
                                     log_level='debug' if config['debug'] else 'warning',
                                     reload=config['reload'],
                                     reload_includes=['*.py', '*.css']
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
        server = Server(config=self.config)
        if self.config.should_reload:
            sock = self.config.bind_socket()
            self.uvicorn_instance = ChangeReload(self.config, target=server.run, sockets=[sock])
        elif self.config.workers > 1:
            sock = self.config.bind_socket()
            self.uvicorn_instance = Multiprocess(self.config, target=server.run, sockets=[sock])
        else:
            self.uvicorn_instance = server
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


_servers = {}


def init():
    """ Initializes the servers. """
    logger.info(' > Loading server')
    for server_type in ['ui', 'api']:
        config = mergedeep.merge(CONFIG.get('global')[server_type], {'debug': CONFIG.get('global')['debug']})
        if config['enabled']:
            factory = f'hermes.core.server:init_{server_type}'
            # @todo Can we find a way to have a hot reload API ?
            if server_type == 'api':
                config['reload'] = False
                factory = init_api()
            _servers[server_type] = _ServerThread(factory, config)


def init_ui():
    """
    Factory method for the uvicorn API server.
    @see --factory option in uvicorn: https://www.uvicorn.org/#application-factories
    """
    return ui.init()


def init_api():
    """
    Factory method for the uvicorn API server.
    @see --factory option in uvicorn: https://www.uvicorn.org/#application-factories
    """
    return api.init()


def start():
    """ Starts the webserver. """
    start_api = CONFIG.get('global')['api']['enabled']
    start_ui = CONFIG.get('global')['ui']['enabled']
    auto_open = start_ui and CONFIG.get('global')['ui']['open']

    logger.info(f' > Start server  '
                f'{"-with API-" if start_api else ""} '
                f'{"-with GUI" if start_ui else ""}'
                f'{" (auto-open)-" if auto_open else "-"}')

    # Auto open the browser.
    if auto_open:
        host = CONFIG.get('global')['ui']['host']
        port = CONFIG.get('global')['ui']['port']
        # @todo: certificate to use the GUI through https.
        webbrowser.open(f'http://{host if host != "0.0.0.0" else "127.0.0.1"}:{port}/')

    # Start the servers.
    for server_type in ['ui', 'api']:
        if CONFIG.get('global')[server_type]['enabled']:
            _servers[server_type].start()


def close():
    """ Stops the webserver. """
    logger.info(' > Close the servers')
    for server_type in ['ui', 'api']:
        if _servers[server_type].is_alive():
            _servers[server_type].close()
            _servers[server_type].join()
            logger.debug(f'    - Server {server_type} is now closed.')
