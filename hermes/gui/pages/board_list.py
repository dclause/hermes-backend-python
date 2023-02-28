""" Board list page. """
from nicegui import ui

from hermes.gui import AbstractPage, pages


@pages.page(path='/boards', title='Mes cartes')
class BoardListPage(AbstractPage):
    """ Board list page """

    def content(self) -> None:
        ui.label('Hello!')
