"""
DigitalWrite Command: simple command attached to digitalPin.

code: MessageCode::BOOLEAN_OUTPUT
"""

from hermes.devices import AbstractDevice
from hermes.core.dictionary import MessageCode


class BooleanOutputDevice(AbstractDevice):
    """ BooleanOutputDevice device: toggles a pin value on/off. """

    def __init__(self):
        super().__init__()
        self.pin: int = 0

    @property
    def code(self) -> MessageCode:
        return MessageCode.BOOLEAN_OUTPUT

    def _encode_settings(self) -> bytearray:
        return bytearray([self.pin, self.default])

    def _encode_value(self, value: any) -> bytearray:
        return bytearray([value])


class BooleanInputDevice(AbstractDevice):
    """ BooleanInputDevice command: reads the on/off state of a pin. """

    @property
    def code(self) -> MessageCode:
        return MessageCode.BOOLEAN_INPUT

    def _encode_settings(self) -> bytearray:
        return bytearray()

    def _encode_value(self, value: any) -> bytearray:
        return bytearray()
