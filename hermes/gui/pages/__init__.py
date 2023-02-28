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

    def build(self):
        """
        Build the page main layout.
        This method _can_ be overriden but is not meant to.
        """
        with layout.layout():
            ui.label(self.title).classes('text-3xl md:text-5xl font-medium mt-[-12px]')
            self.content()

    @abstractmethod
    def content(self) -> None:
        """
        Each page type must implement the content method to build the GUI associated with the page.
        @see https://nicegui.io/
        """
