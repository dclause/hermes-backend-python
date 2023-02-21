from contextlib import contextmanager
from pathlib import Path

from nicegui import ui
from nicegui.element import Element

from hermes import __name__
from hermes.ui import svg

STYLE = '''
<style>
    @keyframes star-tumble {
          0% { transform: translateX(2em) rotate(144deg); }
        100% { transform: translateX(0)   rotate(0);      }
    }
    @keyframes star-pulse {
          0% { scale: 1.0; }
         60% { scale: 1.0; }
         70% { scale: 1.2; }
         80% { scale: 1.0; }
         90% { scale: 1.2; }
        100% { scale: 1.0; }
    }
    .star {
        height: 1.75em;
        fill: white;
        animation: 1s ease-in-out 6s both star-tumble,
                   3s ease-in-out 3s infinite star-pulse;
    }
    .star:hover {
        fill: rgb(250 204 21);
    }

    @keyframes star-grow {
          0% { width: 0 }
        100% { width: 2em }
    }
    .star-container {
        animation: 1s ease-in-out 6s both star-grow;
    }
</style>
'''

STAR = '''
<svg viewBox="0 0 16 16">
    <path d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25zm0 2.445L6.615 5.5a.75.75 0 01-.564.41l-3.097.45 2.24 2.184a.75.75 0 01.216.664l-.528 3.084 2.769-1.456a.75.75 0 01.698 0l2.77 1.456-.53-3.084a.75.75 0 01.216-.664l2.24-2.183-3.096-.45a.75.75 0 01-.564-.41L8 2.694v.001z"></path>
</svg>
'''


@contextmanager
def frame(menu_items: dict = None):
    """ Custom page frame to share the same styling and behavior across all pages """

    if menu_items is None:
        menu_items = {}

    ui.colors(primary='#5898d4', secondary='#53B689', accent='#111B1E', positive='#53B689')
    ui.add_head_html(f"<style>{(Path(__file__).parent / 'static' / 'style.css').read_text()}</style>")
    ui.add_head_html(STYLE)

    with ui.header().classes('items-center duration-200 p-0 px-4 no-wrap').style(
            'box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1)'):
        # LOGO + TITLE with link to homepage
        with ui.link(target='/').classes('row gap-4 items-center no-wrap mr-auto'):
            svg.logo().classes('w-8 stroke-white stroke-2')
            ui.label(__name__).classes('text-xl sm:text-2xl md:text-3xl leading-7')

        # MENU
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
            svg.github().classes('fill-white scale-125 m-1')

        # STAR LOGO
        with ui.link(target='https://github.com/dclause/hermes', new_tab=True).classes('star-container'):
            with Element('svg').props('viewBox="0 0 24 24"').classes('star'):
                Element('path').props(
                    'd="M23.555,8.729a1.505,1.505,0,0,0-1.406-.98H16.062a.5.5,0,0,1-.472-.334L13.405,1.222a1.5,1.5,0,0,0-2.81,0l-.005.016L8.41,7.415a.5.5,0,0,1-.471.334H1.85A1.5,1.5,0,0,0,.887,10.4l5.184,4.3a.5.5,0,0,1,.155.543L4.048,21.774a1.5,1.5,0,0,0,2.31,1.684l5.346-3.92a.5.5,0,0,1,.591,0l5.344,3.919a1.5,1.5,0,0,0,2.312-1.683l-2.178-6.535a.5.5,0,0,1,.155-.543l5.194-4.306A1.5,1.5,0,0,0,23.555,8.729Z"')
            with ui.tooltip('').classes('bg-[#486991] w-96 p-4'):
                with ui.row().classes('items-center no-wrap'):
                    svg.logo().classes('w-14 stroke-white stroke-[1pt]')
                    with ui.column().classes('p-2 gap-2'):
                        ui.label('Star us on GitHub!').classes('text-[180%]')
                        ui.label('And tell others about HERMES.').classes('text-[140%]')
    with ui.row().classes('absolute-center'):
        yield
