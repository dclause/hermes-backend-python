"""
DigitalWrite Command: simple command attached to digitalPin.

code: MessageCode::BOOLEAN_OUTPUT
"""
from collections.abc import Callable
from typing import Any

from nicegui import ui

from hermes.core.dictionary import MessageCode
from hermes.devices import AbstractDevice


class BooleanOutputDevice(AbstractDevice):
    """BooleanOutputDevice device: toggles a pin value on/off."""

    def __init__(self) -> None:
        super().__init__(False)
        self.pin: int = 0

    @property
    def code(self) -> MessageCode:  # noqa: D102
        return MessageCode.BOOLEAN_OUTPUT

    def _encode_data(self) -> bytearray:
        return bytearray([self.pin, self.default])

    def _encode_value(self, value: Any) -> bytearray:
        return bytearray([value])

    def render_info(self) -> None:  # noqa: D102
        ui.label(f'(pin: {self.pin})')

    def render_action(self, mutator: Callable[[int, Any], None]) -> None:  # noqa: D102
        ui.switch(on_change=lambda: mutator(self.id, self.state)) \
            .props('dense keep-color color="primary" size="xl"') \
            .bind_value(self, 'state')


class BooleanInputDevice(AbstractDevice):
    """BooleanInputDevice command: reads the on/off state of a pin."""

    @property
    def code(self) -> MessageCode:  # noqa: D102
        return MessageCode.BOOLEAN_INPUT

    def _encode_data(self) -> bytearray:
        return bytearray()

    def _encode_value(self, value: Any) -> bytearray:
        return bytearray()
