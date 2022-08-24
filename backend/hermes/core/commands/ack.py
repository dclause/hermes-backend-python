"""
ACK Command: acknowledge from the arduino board.

code: MessageCode::ACK
"""

from hermes.core.commands import AbstractCommand
from hermes.core.dictionary import MessageCode


class AckCommand(AbstractCommand):
    """ ACK command. """

    @property
    def code(self) -> MessageCode:
        return MessageCode.ACK
