"""
LED device: this device represents a simple LED.
https://en.wikipedia.org/wiki/Light-emitting_diode.
"""

from hermes import gui
from hermes.devices.boolean import BooleanOutputDevice


class LedDevice(BooleanOutputDevice):
    """LED class."""

    @classmethod
    def render_icon(cls) -> str:  # noqa: D102
        gui.icon('led', 30, 30)
        return ''
