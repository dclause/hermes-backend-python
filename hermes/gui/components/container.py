"""Provide a container with a custom tag."""

from nicegui.element import Element


class Container(Element):
    """Provide a container with a custom tag."""

    def __init__(self, tag: str = 'div') -> None:
        super().__init__(tag)
