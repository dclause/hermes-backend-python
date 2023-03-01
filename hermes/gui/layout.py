from contextlib import contextmanager
from pathlib import Path

from nicegui import ui

from hermes import __app__, __tagline__
from hermes.gui import icon


@contextmanager
def _header(menu_items: dict = None):
    """ Header default layout and styling. """

    if menu_items is None:
        menu_items = {}

    ui.colors(
        primary='#1976D2',
        secondary='#424242',
        accent='#82B1FF',
        positive='#4CAF50',
        negative='#FF5252',
        info='#2196F3',
        warning='#FFC107'
    )
    ui.add_head_html(f"<style>{(Path(__file__).parent / 'static' / 'style.css').read_text()}</style>")
    ui.add_head_html(f"<style>{(Path(__file__).parent / 'static' / 'quasar-overrides.css').read_text()}</style>")

    with ui.header(elevated=True).classes('items-center duration-200 p-1 px-4 no-wrap'):

        ######
        # TITLE with link to homepage
        with ui.link(target='/').classes('row gap-4 items-center no-wrap mr-auto'):
            ui.label(__app__).classes('text-2xl leading-7')
            ui.label(f'- {__tagline__}').classes('hide md:block text-2xl leading-7')

        # MENU on header
        with ui.row().classes('lg:hidden'):
            with ui.menu().classes('bg-primary text-white text-lg') as menu:
                for item_title, item_target in menu_items.items():
                    ui.menu_item(item_title, on_click=lambda _, target=item_target: ui.open(target))
            ui.button(on_click=menu.open).props('flat color=white icon=menu')
        with ui.row().classes('max-lg:hidden'):
            for item_title, item_target in menu_items.items():
                ui.link(item_title, item_target).classes(replace='text-lg text-white')

        # GITHUB LOGO
        with ui.link(target='https://github.com/dclause/hermes', new_tab=True):
            icon.svg('github', 20, 20).classes('fill-white')

        # STAR LOGO
        with ui.link(target='https://github.com/dclause/hermes', new_tab=True).classes('star-container'):
            icon.svg('star', 20, 20).classes('fill-white')
            with ui.tooltip('').classes('bg-[#486991] w-96 p-4'):
                with ui.row().classes('items-center no-wrap'):
                    icon.svg('logo').classes('w-14 stroke-white stroke-[1pt]')
                    with ui.column().classes('p-2 gap-2'):
                        ui.label('Star us on GitHub!').classes('text-[180%]')
                        ui.label('And tell others about HERMES.').classes('text-[140%]')


@contextmanager
def _sidebar(menu_items: dict = None):
    """ Sidebar default layout and styling. """

    with ui.left_drawer(top_corner=True, bottom_corner=True, fixed=True) \
            .props('no-swipe-open no-swipe-close mini behavior=desktop persistent') \
            .classes(add='q-pa-0', remove='q-pa-md'):
        # Logo with link
        with ui.link(target='/').classes('row gap-3 items-center no-wrap q-mr-auto').classes('q-my-md'):
            icon.svg('logo', 50, 50).classes('w-8 stroke-white stroke-2').classes('mx-auto')

        ui.separator().classes(remove='w-full').classes('q-mx-sm q-mb-md')


@contextmanager
def _main():
    """ Main area default layout and styling. """
    with ui.column().classes('w-full p-5 mx-auto'):
        yield


@contextmanager
def layout():
    """ Custom page frame to share the same styling and behavior across all pages """
    _header()
    _sidebar()
    with _main():
        yield
