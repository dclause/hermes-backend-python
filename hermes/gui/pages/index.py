""" Index page. """

from nicegui import ui

from hermes.core.config import settings
from hermes.gui import AbstractPage, pages


@pages.page(path='/', title=None)
class IndexPage(AbstractPage):
    """ Index page """

    def content(self) -> None:
        with ui.row().classes('absolute-center'):
            ui.label('This is the home page.').classes('text-h4 font-bold text-grey-8')

            for _, board in settings.get('boards').items():
                ui.label().bind_text(board, 'name')
                for _, action in board.actions.items():
                    ui.label(action.state).bind_text_from(action, 'state')
