""" Board page. """
from nicegui import ui

from hermes.core.config import settings
from hermes.gui import AbstractPage, pages


@pages.page(path='/board/{bid}')
class BoardPage(AbstractPage):
    """ Board list page """

    # pylint: disable-next=arguments-differ

    def __init__(self):
        super().__init__()
        self.board = None

    def create(self, bid: int):
        """
        :param bid: The board ID (from URL)
        """
        self.board = settings.get(['boards', bid])
        self.title = self.board.name
        self.subtitle = f'{self.board.controller} <em class="pl-1 font-bold">{self.board.model}</em>'
        super().build()

    def content(self) -> None:
        with ui.tabs() \
                .props('inline-label indicator-color="primary"') \
                .classes('text-uppercase text-xl') as tabs:
            ui.tab(label='Information', name='info')
            ui.tab(label='Controls and actions', name='controls')
            ui.tab(label='Sensors and inputs', name='inputs')
            ui.tab(label='History', name='history')

        with ui.tab_panels(tabs, value='controls'):
            with ui.tab_panel(name='info'):
                ui.label('This is the info tab')
            with ui.tab_panel(name='controls'):
                ui.label('This is the controls tab')
            with ui.tab_panel(name='inputs'):
                ui.label('This is the inputs tab')
            with ui.tab_panel(name='history'):
                ui.label('This is the history tab')

    def render_subtitle(self) -> None:
        # ui.label().classes('md:text-lg').bind_text(self.board, 'controller')
        # Tag(tag='em').classes('md:text-lg font-bold').bind_text(self.board, 'model')
        ui.html().classes('md:text-lg').bind_content(self, 'subtitle')
