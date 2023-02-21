from fastapi import FastAPI
from nicegui import ui

from hermes import __name__, __version__
from hermes.core import logger
from hermes.ui import theme


def init(server: FastAPI) -> None:
    logger.info(' > Initialize frontend')

    # ----------------------------------------
    # Web  server route definition
    # ----------------------------------------
    # @todo CORS for the server ?

    @server.get("/healthcheck")
    @server.get("/healthcheck")
    def healthcheck():
        return {
            'status': 'healthy',
            'version': __version__
        }

    @ui.page('/')
    def index_page() -> None:
        with theme.frame():
            ui.label('This is the home page.').classes('text-h4 font-bold text-grey-8')

    ui.run_with(server, title=__name__)
