from contextlib import contextmanager
from pathlib import Path

from nicegui import ui

from hermes import __app__, __tagline__
from hermes.ui import icon


@contextmanager
def default(menu_items: dict = None):
    """ Custom page frame to share the same styling and behavior across all pages """

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

    with ui.header(elevated=True).classes('items-center duration-200 p-1 px-4 no-wrap'):

        ######
        # LEFT DRAWER
        with ui.left_drawer(top_corner=True, bottom_corner=True, fixed=True) \
                .props('no-swipe-open no-swipe-close mini behavior=desktop persistent') \
                .classes(add='q-pa-xs', remove='q-pa-md'):
            with ui.link(target='/').classes('row gap-3 items-center no-wrap mr-auto'):
                icon.svg('logo', 50, 50).classes('w-8 stroke-white stroke-2')
            ui.separator().classes('q-mt-xs q-mb-xs')

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
    with ui.row().classes('absolute-center'):
        yield
