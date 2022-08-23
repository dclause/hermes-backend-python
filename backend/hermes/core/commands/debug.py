"""
DEBUG Command: Displays debug data send from slave board.

code: CommandCode::DEBUG
"""

from hermes.core import logger
from hermes.core.commands import AbstractCommand, CommandCode
from hermes.core.protocols import AbstractProtocol


class DebugCommand(AbstractCommand):
    """ Displays debug data send from slave board. """

    def __init__(self):
        super().__init__()
        self._data = ""

    @property
    def code(self) -> CommandCode:
        return CommandCode.DEBUG

    def _get_settings(self) -> bytearray:
        return bytearray()

    def _get_mutation(self, value: any) -> bytearray:
        return bytearray()

    def receive(self, connexion: AbstractProtocol):
        self._data = connexion.read_line()

    def process(self):
        """ Processes the command """
        logger.info(f'## DEBUG ROBOT: {self._data} ##', )
