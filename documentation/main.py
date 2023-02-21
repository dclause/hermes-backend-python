#!/usr/bin/env python3

"""
@todo describe this.
"""
from pathlib import Path

from nicegui import ui, Client
from pygments.formatters.html import HtmlFormatter

from documentation import svg
from documentation.example import bash_window, browser_window
from documentation.star import add_star
from documentation.style import title, subtitle, link_target, section_heading, features
from hermes import __name__


def add_head_html() -> None:
    ui.add_head_html((Path(__file__).parent / 'static' / 'header.html').read_text())
    ui.add_head_html(f'<style>{HtmlFormatter(nobackground=True).get_style_defs(".codehilite")}</style>')
    ui.add_head_html(f"<style>{(Path(__file__).parent / 'static' / 'style.css').read_text()}</style>")


def add_header() -> None:
    menu_items = {
        'Features': '/#features',
        'Installation': '/#installation',
        'Concepts': '/#concepts',
    }
    with ui.header() \
            .classes('items-center duration-200 p-0 px-4 no-wrap') \
            .style('box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1)'):
        with ui.link(target=index_page).classes('row gap-4 items-center no-wrap mr-auto'):
            svg.logo().classes('w-8 stroke-white stroke-2')
            ui.label(__name__).classes('text-xl sm:text-2xl md:text-3xl leading-7')

        with ui.row().classes('lg:hidden'):
            with ui.menu().classes('bg-primary text-white text-lg') as menu:
                for item_title, item_target in menu_items.items():
                    ui.menu_item(item_title, on_click=lambda _, target=item_target: ui.open(target))
            ui.button(on_click=menu.open).props('flat color=white icon=menu')
        with ui.row().classes('max-lg:hidden'):
            for item_title, item_target in menu_items.items():
                ui.link(item_title, item_target).classes(replace='text-lg text-white')
        with ui.link(target='https://github.com/dclause/hermes', new_tab=True):
            svg.github().classes('fill-white scale-125 m-1')
        add_star()


@ui.page('/')
async def index_page(client: Client):
    """ Index page for documentation. """
    client.content.classes(remove='q-pa-md gap-4')
    add_head_html()
    add_header()

    with ui.row().classes('w-full h-screen items-center gap-8 pr-4 no-wrap into-section'):
        svg.logo().classes('stroke-black w-[400px] md:w-[460px] lg:w-[600px] -ml-[200px] md:-ml-[230px] lg:-ml-[300px]')
        with ui.column().classes('gap-4 md:gap-8 pt-32'):
            title('Meet *HERMES*.')
            subtitle("And let any browser be the frontend of your robots.") \
                .classes('max-w-[20rem] sm:max-w-[24rem] md:max-w-[30rem]')
            ui.link(target='#features').classes('scroll-indicator')

    with ui.column().classes('w-full p-8 lg:p-16 bold-links arrow-links max-w-[1600px] mx-auto'):
        link_target('features', '-50px')
        section_heading('Features', 'HERMES *nicely*')
        with ui.row().classes('w-full text-lg leading-tight grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-8'):
            features('memory', 'Boards & Protocols', [
                'All arduino boards supported at the time',
                'Communication is done by the serial port',
                'Others can be easily added'
            ])
            features('source', 'Modular', [
                'HERMES is designed with modularity in mind',
                'Create a module and extend the framework',
                'Extend the IU',
                'Add new boards, protocols or commands',
            ])
            features('swap_horiz', 'Interaction', [
                'buttons, switches, sliders, inputs and outputs, ...',
                'all with nice UI elements'
                'helps you interact with your boards',
            ])
            features('anchor', 'Foundation', [
                'UI is bridged from Python by [NiceGUI](https://nicegui.io/)',
                'it uses a generic [Vue](https://vuejs.org/) tech under hood',
                'and components from [Quasar](https://quasar.dev/)',
                'all served with [FastAPI](http://fastapi.tiangolo.com/)',
                'Python 3.10+',
            ])

    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1600px] mx-auto'):
        link_target('installation', '-50px')
        section_heading('Installation', 'Get *started*')
        with ui.row().classes('w-full text-lg leading-tight grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8'):
            with ui.column().classes('w-full max-w-md gap-2'):
                ui.html('<em>1.</em>').classes('text-3xl font-bold')
                ui.markdown('Clone the repository').classes('text-lg')
                with bash_window(classes='w-full h-52'):
                    ui.markdown('''```bash\n
git clone https://github.com/dclause/hermes.git
cd hermes
```''')

            with ui.column().classes('w-full max-w-md gap-2'):
                ui.html('<em>2.</em>').classes('text-3xl font-bold')
                ui.markdown('Install & launch').classes('text-lg')
                with bash_window(classes='w-full h-52'):
                    ui.markdown('''```bash\n
python3 -m venv .venv
source ./.venv/Scripts/activate
pip install -r requirements.txt
pip install -r dev_requirements.txt

python -m hermes --ui
```''')

            with ui.column().classes('w-full max-w-md gap-2'):
                ui.html('<em>3.</em>').classes('text-3xl font-bold')
                ui.markdown('Enjoy!').classes('text-lg')
                with browser_window(classes='w-full h-52'):
                    ui.label('Hello HERMES!')

        with ui.expansion('...or use make to help you out...').classes('w-full gap-2 bold-links arrow-links text-lg'):
            with ui.row().classes('mt-8 w-full justify-center items-center gap-8'):
                with bash_window(classes='max-w-2xl w-full h-52'):
                    ui.markdown('```bash\n'
                                'make help\n'
                                'make venv\n'
                                'make install\n'
                                'make run\n'
                                'make doc\n'
                                '```')
                with bash_window(classes='max-w-2xl w-full'):
                    ui.markdown('''```
Available commands:
help                      Print help for each target
documentation             Open documentation
install                   Install everything
run                       Run the code
env                       Source the virtual environment
debug                     Debug the code
clean                     Cleanup
test                      Run all tests
lint                      Lint the code
deps-install              Install the dependencies
dev-deps-install          Install the dev dependencies
deps-update               Update the dependencies
dev-deps-update           Update the dependencies
feedback                  Provide feedback
```''')


ui.run(title="HERMES - Documentation", favicon='static/favicon.ico')
