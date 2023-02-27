"""
GUI package.
This package contains all definition and GUI specific implementation.
"""

from fastapi import FastAPI
from nicegui import ui

from hermes import __app__, __tagline__, __version__
from hermes.core.config import CONFIG
from hermes.gui import layout
from hermes.gui.pages import AbstractPage


def init(app: FastAPI) -> None:
    """ Defines and attaches the GUI routes associated with a fastAPI server. """

    @ui.page('/')
    def index_page() -> None:
        with layout.layout():
            with ui.row().classes('absolute-center'):
                ui.label('This is the home page.').classes('text-h4 font-bold text-grey-8')

                for _, board in CONFIG.get('boards').items():
                    ui.label().bind_text(board, 'name')
                    for _, action in board.actions.items():
                        ui.label(action.state).bind_text_from(action, 'state')

        # layout.header()
        # with layout.sidebar():
        #     with ui.column():
        #         with ui.tabs().props('vertical indicator-color="primary"').classes('full-width') as tabs:
        #             ui.tab(name="tool1", icon='home').props(remove='label')
        #             ui.tab(name="tool2", icon='info').props(remove='label')
        #
        # with ui.row().classes('absolute-center'):
        #     ui.label('This is the home page.').classes('text-h4 font-bold text-grey-8')
        #     with ui.column():
        #         with ui.tab_panels(tabs, value='tool1').props('vertical'):
        #             with ui.tab_panel(name="tool1"):
        #                 ui.label('This is the first tab')
        #             with ui.tab_panel(name="tool2"):
        #                 ui.label('This is the second tab')

    # for page in AbstractPage.plugins:
    #     page.create()

    ui.run_with(app, title=f'{__app__} - {__tagline__}')
