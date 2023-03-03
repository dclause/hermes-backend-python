"""
GUI package.
This package contains all definition and GUI specific implementation.
"""

from fastapi import FastAPI
from nicegui import ui

from hermes import __app__, __tagline__
from hermes.gui import layout
from hermes.gui.pages import AbstractPage
from .components.container import Container as container
from .components.icon import Icon as icon
from .components.tag import Tag as tag

CLIENT_ID = __app__


def init(app: FastAPI) -> None:
    """ Defines and attaches the GUI routes associated with a fastAPI server. """

    for page in AbstractPage.plugins:
        ui.page(page.path)(page().create)

    ui.run_with(app, title=f'{__app__} - {__tagline__}')
