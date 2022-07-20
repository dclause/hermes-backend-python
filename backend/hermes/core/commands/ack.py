"""
ACK Command: acknowledge from the arduino board.

code: CommandCode::ACK
"""

from hermes.core.commands import AbstractCommand, CommandCode


class BlinkCommand(AbstractCommand):
    """ ACK command. """

    @property
    def code(self) -> CommandCode:
        return CommandCode.ACK
