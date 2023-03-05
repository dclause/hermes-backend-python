"""Contain all definition and GUI specific implementation."""

from fastapi import FastAPI
from nicegui import ui

from hermes import __app__, __tagline__
from hermes.gui.pages import AbstractPage

# Follow nicegui.io convention on imports for components.
from .components.container import Container as container  # noqa: N813, F401
from .components.icon import Icon as icon  # noqa: N813, F401
from .components.tag import Tag as tag  # noqa: N813, F401

CLIENT_ID = __app__


def init(app: FastAPI) -> None:
    """Define and attach the GUI routes associated with a fastAPI server."""

    for page in AbstractPage.plugins:
        ui.page(page.path)(page().create)

    ui.run_with(app, title=f'{__app__} - {__tagline__}')


__ALL__ = ['CLIENT_ID', 'init']
