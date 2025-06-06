"""
SERVO Command: Orders a servo to move to given position.

code: MessageCode::SERVO
"""
from collections.abc import Callable
from typing import Any

from nicegui import ui

from hermes import gui
from hermes.core.dictionary import MessageCode
from hermes.devices import AbstractDevice


class ServoDevice(AbstractDevice):
    """Sends a Servo command."""

    def __init__(self) -> None:
        super().__init__(0)
        self.pin: int = 0
        self.tmin: int = 0
        self.tmax: int = 180
        self.min: int = 0
        self.max: int = 180
        self.speed: int = -1
        self.acceleration: int = -1

    @property
    def code(self) -> MessageCode:  # noqa: D102
        return MessageCode.SERVO

    def render_icon(self) -> str:  # noqa: D102
        gui.icon('servo', 30, 40)
        return ''

    def render_info(self) -> None:  # noqa: D102
        ui.label(f'(pin: {self.pin})')

    def render_action(self, mutator: Callable[[int, Any], None]) -> None:  # noqa: D102
        # with ui.column():
        ui.slider(min=self.min, max=self.max, value=self.state) \
            .on('change', lambda value: mutator(self.id, value['args'])) \
            .props('label') \
            .bind_value(self, 'state')
        # ui.number(value=self.state, on_change=lambda value: mutator(self.id, value)) \
        #     .bind_value(self, 'state')

    def _encode_data(self) -> bytearray:
        return bytearray([self.pin]) + \
            self._encode_value(self.default) + \
            self._encode_value(self.tmin) + \
            self._encode_value(self.tmax) + \
            self._encode_value(self.min) + \
            self._encode_value(self.max) + \
            self._encode_value(self.speed, signed=True) + \
            self._encode_value(self.acceleration, signed=True)

    def _encode_value(self, value: int, signed: bool = False) -> bytearray:
        return bytearray(value.to_bytes(2, byteorder='big', signed=signed))
