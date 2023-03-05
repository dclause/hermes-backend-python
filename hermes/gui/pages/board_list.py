""" Board list page. """
from nicegui import ui

from hermes.core.config import settings
from hermes.gui import AbstractPage, pages


@pages.page(path='/boards', title='My boards', subtitle='test a subtitle')
class BoardListPage(AbstractPage):
    """ Board list page. """

    def content(self) -> None:
        for _, board in settings.get('boards').items():
            ui.label().bind_text(board, 'name')
            for _, action in board.actions.items():
                ui.icon('view_in_ar')
                ui.label(action.state).bind_text_from(action, 'state')
