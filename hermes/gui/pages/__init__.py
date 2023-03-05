"""
Page plugin type definition.

This plugin let you create new pages within the app.
The creation of a new page should be done as follows:

Example:
-------
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


def page(path: str, title: Optional[str] = None, subtitle: Optional[str] = None):
    """ Decorator to add properties to a AbstractPage subclass implementation. """

    def decorator(klass):
        klass.path = path
        klass.title = title
        klass.subtitle = subtitle
        return klass

    return decorator


class AbstractPage(AbstractPlugin, metaclass=MetaPluginType):
    """ Manages plugins of type commands. """

    path = None
    title = None
    subtitle = None

    def create(self):
        """
        Creates the page as of nicegui method definition.
        @see https://nicegui.io/reference#page
        @see https://nicegui.io/reference#pages_with_path_parameters.
        """
        self.build()

    def build(self) -> None:
        """
        Build the page main layout.
        While this _can_ be overriden but is not meant to.
        """
        with layout.layout():
            with ui.column().classes(remove='gap-4'):
                self.render_title()
                self.render_subtitle()
            self.content()

    @abstractmethod
    def content(self) -> None:
        """
        Each page type must implement the content method to build the GUI associated with the page.
        @see https://nicegui.io/.
        """

    def render_title(self) -> None:
        """ Renders the title. """
        if self.title:
            ui.label().classes('text-2xl md:text-4xl').bind_text(self, 'title')

    def render_subtitle(self) -> None:
        """ Renders the subtitle. """
        if self.subtitle:
            ui.label().classes('font-light text-overline text-uppercase').bind_text(self, 'subtitle')


__ALL__ = ['page', 'AbstractPage']
