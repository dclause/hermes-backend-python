import re
from typing import Optional


from nicegui import ui

REGEX_H4 = re.compile(r'<h4.*?>(.*?)</h4>')
SPECIAL_CHARACTERS = re.compile('[^(a-z)(A-Z)(0-9)-]')
PYTHON_BGCOLOR = '#00000010'
PYTHON_COLOR = '#eef5fb'
BASH_BGCOLOR = '#00000010'
BASH_COLOR = '#e8e8e8'
BROWSER_BGCOLOR = '#00000010'
BROWSER_COLOR = '#ffffff'


def remove_prefix(text: str, prefix: str) -> str:
    return text[len(prefix):] if text.startswith(prefix) else text

def _window_header(bgcolor: str) -> ui.row():
    return ui.row().classes(f'w-full h-8 p-2 bg-[{bgcolor}]')


def _dots() -> None:
    with ui.row().classes('gap-1 relative left-[1px] top-[1px]'):
        ui.icon('circle').classes('text-[13px] text-red-400')
        ui.icon('circle').classes('text-[13px] text-yellow-400')
        ui.icon('circle').classes('text-[13px] text-green-400')


def _title(title: str) -> None:
    ui.label(title).classes('text-sm text-gray-600 absolute left-1/2 top-[6px]').style('transform: translateX(-50%)')


def _tab(name: str, color: str, bgcolor: str) -> None:
    with ui.row().classes('gap-0'):
        with ui.label().classes(f'w-2 h-[24px] bg-[{color}]'):
            ui.label().classes(f'w-full h-full bg-[{bgcolor}] rounded-br-[6px]')
        ui.label(name).classes(f'text-sm text-gray-600 px-6 py-1 h-[24px] rounded-t-[6px] bg-[{color}]')
        with ui.label().classes(f'w-2 h-[24px] bg-[{color}]'):
            ui.label().classes(f'w-full h-full bg-[{bgcolor}] rounded-bl-[6px]')


def window(color: str, bgcolor: str, *, title: str = '', tab: str = '', classes: str = '') -> ui.column:
    with ui.card().classes(f'no-wrap bg-[{color}] rounded-xl p-0 gap-0 {classes}') \
            .style('box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1)'):
        with _window_header(bgcolor):
            _dots()
            if title:
                _title(title)
            if tab:
                _tab(tab, color, bgcolor)
        return ui.column().classes('w-full h-full overflow-auto')


def python_window(*, classes: str = '') -> ui.card:
    return window(PYTHON_COLOR, PYTHON_BGCOLOR, title='main.py', classes=classes).classes('p-2 python-window')


def bash_window(*, classes: str = '') -> ui.card:
    return window(BASH_COLOR, BASH_BGCOLOR, title='bash', classes=classes).classes('p-2 bash-window')


def browser_window(title: Optional[str] = None, *, classes: str = '') -> ui.card:
    return window(BROWSER_COLOR, BROWSER_BGCOLOR, tab=title or 'NiceGUI', classes=classes).classes('p-4 browser-window')
