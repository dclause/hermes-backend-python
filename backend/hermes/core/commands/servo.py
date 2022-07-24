"""
SERVO Command: Orders a servo to move to given position.

code: CommandCode::SERVO
"""

from hermes.core.commands import AbstractCommand, CommandCode


class ServoAction(AbstractCommand):
    """ Sends a Servo command """

    @property
    def code(self) -> CommandCode:
        return CommandCode.SERVO

    @property
    def _is_runnable(self) -> bool:
        return True
