"""
BLINK Command: blinks a LED.

code: CommandCode::BLINK
"""

from hermes.core.commands import AbstractCommand, CommandCode


class BlinkCommand(AbstractCommand):
    """ Blinks a led. """

    @property
    def code(self) -> CommandCode:
        return CommandCode.BLINK
