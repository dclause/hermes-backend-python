"""
ACK Command: acknowledge from the arduino board.

code: CommandCode::ACK
"""
from enum import Enum

from hermes.core.commands import AbstractCommand, CommandCode


class BlinkCommand(AbstractCommand):
    """ ACK command. """

    @property
    def __type__(self) -> Enum:
        # @todo here the type is a code: rethink this.
        return CommandCode.ACK

    def __init__(self):
        super().__init__(CommandCode.ACK, 'ACK')
