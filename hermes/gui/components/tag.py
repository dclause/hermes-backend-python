"""Displays some text, wrapped in custom tag."""
from typing import Any

from nicegui.elements.mixins.text_element import TextElement


class Tag(TextElement):  # type: ignore[misc]
    """Displays some text, wrapped in custom tag."""

    def __init__(self, *, tag: str = 'div', text: str = '', **kwargs: Any) -> None:
        super().__init__(tag=tag, text=text, **kwargs)
