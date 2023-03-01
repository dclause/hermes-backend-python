""" Board list page. """
from nicegui import ui

from hermes.core.config import settings
from hermes.gui import AbstractPage, pages


@pages.page(path='/boards', title='Mes cartes')
class BoardListPage(AbstractPage):
    """ Board list page """

    def content(self, *args, **kwargs) -> None:
        for _, board in settings.get('boards').items():
            ui.label().bind_text(board, 'name')
            for _, action in board.actions.items():
                ui.label(action.state).bind_text_from(action, 'state')
