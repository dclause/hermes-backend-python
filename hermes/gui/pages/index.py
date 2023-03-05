""" Index page. """

from nicegui import ui

from hermes.gui import AbstractPage, pages


@pages.page(path='/', title=None)
class IndexPage(AbstractPage):
    """ Index page. """

    def content(self) -> None:
        with ui.row().classes('absolute-center'):
            ui.label('Welcome to HERMES').classes('text-h4 font-bold text-grey-8')
