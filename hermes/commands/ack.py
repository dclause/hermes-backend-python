"""
ACK Command: acknowledge from the arduino board.

code: MessageCode::ACK
"""
from hermes.commands import AbstractCommand
from hermes.core.dictionary import MessageCode


class AckCommand(AbstractCommand):
    """ ACK command. """

    @property
    @override
    def code(self) -> MessageCode:
        return MessageCode.ACK
