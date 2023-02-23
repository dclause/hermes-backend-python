"""
UI package.
This package contains all definition and UI specific implementation.
"""

from fastapi import FastAPI
from nicegui import ui

from hermes import __app__, __tagline__, __version__
from hermes.ui import layout


def init() -> FastAPI:
    """ Defines and returns the UI routes associated with a fastAPI server. """

    app = FastAPI()

    @app.get("/version")
    def healthcheck():
        return {'status': 'healthy', 'version': __version__}

    @ui.page('/')
    def index_page() -> None:
        with layout.default():
            ui.label('This is the home page.').classes('text-h4 font-bold text-grey-8')

    ui.run_with(app, title=f'{__app__} - {__tagline__}')

    return app
