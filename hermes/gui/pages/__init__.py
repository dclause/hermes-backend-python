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
from __future__ import annotations

from abc import abstractmethod
from collections.abc import Callable
from typing import Any

from nicegui import ui

from hermes.core.plugins import AbstractPlugin
from hermes.core.struct import MetaPluginType
from hermes.gui import layout


def page(path: str,
         title: str | None = None,
         subtitle: str | None = None) -> Callable[[AbstractPage], AbstractPage]:
    """Add properties to a AbstractPage subclass implementation."""

    def decorator(klass: AbstractPage) -> AbstractPage:
        klass.path = path
        klass.title = title
        klass.subtitle = subtitle
        return klass

    return decorator


class AbstractPage(AbstractPlugin, metaclass=MetaPluginType):
    """Manage plugins of type commands."""
    path: str | None
    title: str | None
    subtitle: str | None

    def __init__(self) -> None:
        super().__init__()

    def create(self) -> None:
        # @todo def create(self, *arg, **kwarg) -> None: issue to nicegui.io
        """
        Create the page as of nicegui method definition.
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
            with ui.column().classes('mb-4'):
                self.render_title()
                self.render_subtitle()
            self.content()

    @abstractmethod
    def content(self, *args: Any, **kwargs: Any) -> None:
        """
        Each page type must implement the content method to build the GUI associated with the page.
        @see https://nicegui.io/.
        """

    def render_title(self) -> None:
        """Render the title."""
        if self.title:
            ui.label().classes('text-2xl md:text-4xl').bind_text(self, 'title')

    def render_subtitle(self) -> None:
        """Render the subtitle."""
        if self.subtitle:
            ui.label().classes('font-light text-overline text-uppercase').bind_text(self, 'subtitle')


__ALL__ = ['page', 'AbstractPage']
