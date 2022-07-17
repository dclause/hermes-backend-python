"""
DEBUG Command: Displays debug data send from slave board.

code: CommandCode::DEBUG
"""
from enum import Enum

from hermes.core import logger
from hermes.core.commands import AbstractCommand, CommandCode
from hermes.core.protocols import AbstractProtocol


class DebugCommand(AbstractCommand):
    """ Displays debug data send from slave board. """

    @property
    def __type__(self) -> Enum:
        # @todo here the type is a code: rethink this.
        return CommandCode.DEBUG

    def __init__(self):
        super().__init__(CommandCode.DEBUG, 'DEBUG')
        self._data = ""

    def receive(self, connexion: AbstractProtocol):
        self._data = connexion.read_line()

    def process(self):
        """ Processes the command """
        logger.info(f'## DEBUG ROBOT: {self._data} ##', )
