"""Displays some text, wrapped in custom tag."""

from pathlib import Path

from nicegui.elements.mixins.content_element import ContentElement

from hermes.core.helpers import APP_DIR


class Icon(ContentElement):
    """Displays some text, wrapped in custom tag."""

    def __init__(self, name: str, width: int = 50, height: int = 50,
                 path: Path = None) -> None:

        if path is None:
            path = Path(APP_DIR, 'gui', 'static', 'icons')

        svg = Path(path, f'{name}.svg')
        if svg.exists():
            super().__init__(tag='div', content=svg.read_text(encoding='utf-8'))
            self.classes('flex').style(f'width:{width}px;height:{height}px')
        else:
            super().__init__(tag='q-icon', content=name)
            self._props['name'] = name
