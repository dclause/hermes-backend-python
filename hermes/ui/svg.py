from pathlib import Path

from nicegui import ui

PATH = Path(__file__).parent / 'static'


def logo() -> ui.html:
    return ui.html((PATH / 'logo.svg').read_text())


def github() -> ui.html:
    return ui.html((PATH / 'github.svg').read_text())
