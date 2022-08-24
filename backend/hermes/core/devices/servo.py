"""
SERVO Command: Orders a servo to move to given position.

code: MessageCode::SERVO
"""

from hermes.core.devices import AbstractDevice
from hermes.core.dictionary import MessageCode


class ServoDevice(AbstractDevice):
    """ Sends a Servo command """

    def __init__(self):
        super().__init__()
        self.pin: int = 0
        self.min: int = 0
        self.max: int = 180

    @property
    def code(self) -> MessageCode:
        return MessageCode.SERVO

    def _encode_settings(self) -> bytearray:
        return bytearray([self.pin]) + self._encode_value(self.default)

    def _encode_value(self, value: any) -> bytearray:
        return bytearray(value.to_bytes(2, byteorder='big'))
