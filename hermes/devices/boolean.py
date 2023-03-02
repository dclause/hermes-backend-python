"""
DigitalWrite Command: simple command attached to digitalPin.

code: MessageCode::BOOLEAN_OUTPUT
"""
from typing import Any

from nicegui import ui

from hermes.core.config import settings
from hermes.core.dictionary import MessageCode
from hermes.devices import AbstractDevice


class BooleanOutputDevice(AbstractDevice):
    """ BooleanOutputDevice device: toggles a pin value on/off. """

    def __init__(self):
        super().__init__(False)
        self.pin: int = 0

    @property
    def code(self) -> MessageCode:
        return MessageCode.BOOLEAN_OUTPUT

    def _encode_data(self) -> bytearray:
        return bytearray([self.pin, self.default])

    def _encode_value(self, value: any) -> bytearray:
        return bytearray([value])

    # pylint: disable-next=arguments-differ
    def render_info(self):
        ui.label(f'(pin: {self.pin})')

    # pylint: disable-next=arguments-differ
    def render_action(self, board):
        ui.switch(on_change=lambda: self.mutation(0, board.id, self.id, self.value)) \
            .props('dense keep-color color="primary" size="xl"') \
            .bind_value(self, 'value')

    def mutation(self, cid: str, board_id: int, command_id: int, value: Any):
        self.set_value(board_id, value)
        settings.set(['boards', 'actions', command_id], value)


class BooleanInputDevice(AbstractDevice):
    """ BooleanInputDevice command: reads the on/off state of a pin. """

    @property
    def code(self) -> MessageCode:
        return MessageCode.BOOLEAN_INPUT

    def render(self) -> None:
        pass

    def _encode_data(self) -> bytearray:
        return bytearray()

    def _encode_value(self, value: any) -> bytearray:
        return bytearray()
