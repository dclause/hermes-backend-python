from pathlib import Path

from nicegui import ui

PATH = Path(__file__).parent / 'static'

_STAR_STYLE = '''
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
@keyframes star-grow {
      0% { width: 0 }
    100% { width: 2em }
}
.star-container {
    animation: 1s ease-in-out 6s both star-grow;
}
.star {
    animation: 1s ease-in-out 6s both star-tumble,
               3s ease-in-out 3s infinite star-pulse;
}
.star:hover {
    fill: rgb(250 204 21);
}
</style>
'''


def svg(name: str, width: int = 50, height: int = 50) -> ui.html:
    if name is 'start':
        ui.add_head_html(_STAR_STYLE)
    return ui.html((PATH / f'{name}.svg').read_text()).style(f'width:{width}px;height:{height}px')
