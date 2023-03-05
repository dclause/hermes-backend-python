"""Displays some text, wrapped in custom tag."""

from nicegui.elements.mixins.text_element import TextElement


class Tag(TextElement):
    """Displays some text, wrapped in custom tag."""

    def __init__(self, *, tag: str = 'div', text: str = '', **kwargs) -> None:
        super().__init__(tag=tag, text=text)
