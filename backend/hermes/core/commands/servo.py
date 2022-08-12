"""
SERVO Command: Orders a servo to move to given position.

code: CommandCode::SERVO
"""

from hermes.core.commands import AbstractCommand, CommandCode


class ServoAction(AbstractCommand):
    """ Sends a Servo command """

    def __init__(self):
        super().__init__()
        self.min: int = 0
        self.max: int = 180

    @property
    def code(self) -> CommandCode:
        return CommandCode.SERVO

    @property
    def _is_runnable(self) -> bool:
        return True

    # def encode(self, value: any) -> bytearray:
    #     return bytearray(value.to_bytes(2, byteorder='big'))
