"""
ACK Command: acknowledge from the arduino board.

code: CommandCode::ACK
"""

from hermes.core.commands import AbstractCommand, CommandCode


class BlinkCommand(AbstractCommand):
    """ ACK command. """

    def __init__(self):
        super().__init__(CommandCode.ACK, 'ACK')
