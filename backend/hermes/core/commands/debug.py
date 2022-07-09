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
        super().__init__(CommandCode.DEBUG, 'DEBUG')
        self._data = ""

    def receive(self, connexion: AbstractProtocol):
        self._data = connexion.read_line()

    def process(self):
        """ Processes the command """
        logger.debug(f' > start command: {str(self)}', )
        if self._data:
            logger.info(f'## DEBUG command: Received data: {self._data} ##', )
        logger.debug(f' > command done: {str(self)}')
