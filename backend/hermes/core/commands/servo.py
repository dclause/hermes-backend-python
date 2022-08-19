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

    def to_bytes(self) -> bytearray:
        # @todo how to override AbstractCommand more cleverly ?
        header = bytearray([self.code, self.id])
        pindata = bytearray([self.pin])
        data = self.encode(self.default)
        return header + pindata + data

    @property
    def code(self) -> CommandCode:
        return CommandCode.SERVO

    @property
    def _is_runnable(self) -> bool:
        return True

    def encode(self, value: any) -> bytearray:
        return bytearray(value.to_bytes(2, byteorder='big'))
