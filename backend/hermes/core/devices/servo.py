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
        self.tmin: int = 0
        self.tmax: int = 180
        self.min: int = 0
        self.max: int = 180
        self.speed: int = -1
        self.acceleration: int = -1

    @property
    def code(self) -> MessageCode:
        return MessageCode.SERVO

    def _encode_settings(self) -> bytearray:
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
