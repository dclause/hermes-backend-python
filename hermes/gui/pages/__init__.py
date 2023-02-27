from abc import abstractmethod
from typing import Optional

from nicegui import ui

from hermes.core.plugins import AbstractPlugin
from hermes.core.struct import MetaPluginType


class AbstractPage(AbstractPlugin, metaclass=MetaPluginType):
    """ Manages plugins of type commands. """

    def __init__(self, path: str, title: Optional[str] = None) -> None:
        super().__init__()
        self.path = path
        self.title = title

    def create(self) -> None:
        @ui.page(self.path)
        def test() -> None:
            ui.label(self.title).classes('text-3xl md:text-5xl font-medium mt-[-12px]')

    @abstractmethod
    def content(self) -> None:
        """
        Each page type must implement the content method to build the GUI associated with the page.
        @see https://nicegui.io/
        """
        ui.label('Welcome to the other side')
