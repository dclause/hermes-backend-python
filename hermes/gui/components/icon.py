from pathlib import Path

from nicegui import ui

from hermes.core.helpers import APP_DIR

PATH = Path(APP_DIR, 'gui', 'static', 'icons')


def svg(name: str, width: int = 50, height: int = 50) -> ui.html:
    return ui.html(Path(PATH, f'{name}.svg').read_text(encoding="utf-8")).style(f'width:{width}px;height:{height}px')
