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

    def _get_settings(self) -> bytearray:
        return bytearray()

    def _get_mutation(self, value: any) -> bytearray:
        return bytearray()
