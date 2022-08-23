"""
ACK Command: acknowledge from the arduino board.

code: CommandCode::ACK
"""

from hermes.core.commands import AbstractCommand, CommandCode


class AckCommand(AbstractCommand):
    """ ACK command. """

    @property
    def code(self) -> CommandCode:
        return CommandCode.ACK

    def _get_settings(self) -> bytearray:
        return bytearray()

    def _get_mutation(self, value: any) -> bytearray:
        return bytearray()
