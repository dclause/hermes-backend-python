"""
Page plugin type definition.

This plugin let you create new pages within the app.
The creation of a new page should be done as follows:

Example:

.. sourcecode:: python
    @pages.page(path='/foo', title='bar')
    class MyPage(AbstractPage):
        def content(self):
            ui.label('Foo bar is displayed')
``
"""
from abc import abstractmethod
from typing import Optional

from nicegui import ui

from hermes.core.plugins import AbstractPlugin
from hermes.core.struct import MetaPluginType
from hermes.gui import layout


def page(path: str, title: Optional[str] = None):
    """ Decorator to add properties to a AbstractPage subclass implementation. """

    def decorator(klass):
        klass.path = path
        klass.title = title
        return klass

    return decorator


class AbstractPage(AbstractPlugin, metaclass=MetaPluginType):
    """ Manages plugins of type commands. """

    path = None
    title = 'New page'

    def __init__(self):
        super().__init__()
        self.ui_title = None

    def create(self):
        """
        Creates the page as of nicegui method definition.
        @see https://nicegui.io/reference#page
        @see https://nicegui.io/reference#pages_with_path_parameters
        """
        self.build()

    def build(self, *args, **kwargs):
        """
        Build the page main layout.
        While this _can_ be overriden but is not meant to.
        """
        with layout.layout():
            ui.label().classes('text-3xl md:text-5xl font-medium mt-[-12px]').bind_text(self, 'title')
            self.content(*args, **kwargs)

    @abstractmethod
    def content(self, *args, **kwargs) -> None:
        """
        Each page type must implement the content method to build the GUI associated with the page.
        @see https://nicegui.io/
        """
