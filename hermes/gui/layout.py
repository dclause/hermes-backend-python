"""Provide various default layout to guarantee a consistent design across pages."""

from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from nicegui import ui

from hermes import __app__, __tagline__, gui


def _header(menu_items: dict[str, Any] | None = None) -> None:
    """Header default layout and styling."""

    if menu_items is None:
        menu_items = {}

    ui.colors(
        primary='#1976D2',
        secondary='#424242',
        accent='#82B1FF',
        positive='#4CAF50',
        negative='#FF5252',
        info='#2196F3',
        warning='#FFC107',
    )
    ui.add_head_html(f"<style>{(Path(__file__).parent / 'static' / 'style.css').read_text()}</style>")
    ui.add_head_html(f"<style>{(Path(__file__).parent / 'static' / 'overrides.css').read_text()}</style>")
    ui.add_head_html(f"<style>{(Path(__file__).parent / 'static' / 'custom.css').read_text()}</style>")

    with ui.header(elevated=True).classes('items-center duration-200 p-1 px-4 no-wrap'):

        ######
        # TITLE with link to homepage
        with ui.link(target='/').classes('row gap-2 items-center no-wrap mr-auto'):
            ui.label(__app__).classes('text-xl leading-7')
            ui.label(f'- {__tagline__}').classes('hide md:block text-xl leading-7')

        # MENU on header
        # @todo add dynamic menu here
        with ui.row().classes('lg:hidden'):
            with ui.menu().classes('bg-primary text-white text-lg') as menu:
                for item_title, item_target in menu_items.items():
                    ui.menu_item(item_title, on_click=lambda _, target=item_target: ui.open(target))
            ui.button(on_click=menu.open).props('flat color=white icon=menu')
        with ui.row().classes('max-lg:hidden'):
            for item_title, item_target in menu_items.items():
                ui.link(item_title, item_target).classes(replace='text-lg text-white')

        with ui.row().classes(remove='gap-4'):

            # @todo add dynamic menu here
            # ui.button().props('flat round color="white" :size="1rem" icon="shopping_cart"')

            # GITHUB LOGO
            with ui.button() \
                    .props('flat round href="https://github.com/dclause/hermes" target="_blank"'):
                gui.icon('github', 24, 24).classes('fill-white m-2')

            # STAR LOGO
            with ui.button() \
                    .props('flat round href="https://github.com/dclause/hermes" target="_blank"') \
                    .classes('star-container'):
                gui.icon('star', 24, 24).classes('fill-white m-2')
                with ui.tooltip('').classes('bg-[#486991] w-96 p-4'), ui.row().classes('items-center no-wrap'):
                    gui.icon('logo').classes('w-14 stroke-white stroke-[1pt]')
                    with ui.column().classes('p-2 gap-2'):
                        ui.label('Star us on GitHub!').classes('text-[180%]')
                        ui.label('And tell others about HERMES.').classes('text-[140%]')


def _sidebar() -> None:
    """Sidebar default layout and styling."""

    with ui.left_drawer(top_corner=True, bottom_corner=True, fixed=True) \
            .props('no-swipe-open no-swipe-close mini behavior=desktop persistent :mini-width="70"') \
            .classes(add='q-pa-0', remove='q-pa-md'):
        # Logo with link
        with ui.link(target='/').classes('row gap-3 items-center no-wrap q-mr-auto').classes('q-my-md'):
            gui.icon('logo', 50, 50).classes('w-8 stroke-white stroke-2').classes('mx-auto')

        ui.separator().classes(remove='w-full').classes('q-mx-sm q-mb-md')


@contextmanager
def _main() -> Generator[None, None, None]:
    """Content area default layout and styling."""
    with ui.column().classes('full-width full-height p-4 mx-auto', remove='gap-4'):
        yield


@contextmanager
def layout() -> Generator[None, None, None]:
    """Page layout: share the same styling and behavior across all pages."""
    _header()
    _sidebar()
    with _main():
        yield
