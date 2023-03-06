"""Board page."""
from typing import cast

from nicegui import ui

from hermes import gui
from hermes.boards import AbstractBoard
from hermes.core.config import settings
from hermes.gui import AbstractPage, pages


@pages.page(path='/board/{bid}')
class BoardPage(AbstractPage):
    """Board list page."""

    def __init__(self) -> None:
        super().__init__()
        self.board: AbstractBoard | None = None

    def create(self, bid: int) -> None:  # type: ignore[override] # noqa D102 # @todo
        self.board = cast(AbstractBoard, settings.get(['boards', bid]))
        if self.board:
            self.title = self.board.name
            self.subtitle = self.board.controller
        self.build()

    def content(self) -> None:  # noqa: D102
        if not self.board:
            return

        with ui.tabs() \
                .props('inline-label indicator-color="primary"') \
                .classes('text-uppercase text-sm') as tabs:
            ui.tab(label='Information', name='info')
            ui.tab(label='Controls and actions', name='actions')
            ui.tab(label='Sensors and inputs', name='inputs')
            ui.tab(label='History', name='history')

        with ui.card().classes('w-full p-0'), ui.tab_panels(tabs, value='actions').classes('w-full'):
            with ui.tab_panel(name='info'):
                ui.label('This is the info tab')

            # Pane 'controls and actions'
            with ui.tab_panel(name='actions'):
                for _, action in self.board.actions.items():
                    with gui.container().classes('flex items-center no-wrap p-2 board-device'):
                        action.render(self.board.gui_mutator)
                        with gui.container().classes('device-menu'):
                            ui.button().props('round flat icon="more_vert"')
                    ui.separator()

            with ui.tab_panel(name='inputs'):
                ui.label('This is the inputs tab')
            with ui.tab_panel(name='history'):
                ui.label('This is the history tab')

    def render_subtitle(self) -> None:  # noqa: D102
        ui.html().classes('font-light text-overline text-uppercase').bind_content(self, 'subtitle')
