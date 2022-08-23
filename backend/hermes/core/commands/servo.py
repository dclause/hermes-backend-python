"""
SERVO Command: Orders a servo to move to given position.

code: CommandCode::SERVO
"""

from hermes.core.commands import AbstractCommand, CommandCode


class ServoAction(AbstractCommand):
    """ Sends a Servo command """

    def __init__(self):
        super().__init__()
        self.pin: int = -1
        self.min: int = 0
        self.max: int = 180

    @property
    def code(self) -> CommandCode:
        return CommandCode.SERVO

    @property
    def _is_runnable(self) -> bool:
        return True

    def _get_settings(self) -> bytearray:
        return bytearray([self.pin]) + self._encode_value(self.default)

    def _get_mutation(self, value: any) -> bytearray:
        return bytearray([self.id]) + self._encode_value(value)

    @classmethod
    def _encode_value(cls, value: int) -> bytearray:
        return bytearray(value.to_bytes(2, byteorder='big'))
