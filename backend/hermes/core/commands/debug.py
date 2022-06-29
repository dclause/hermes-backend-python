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

    def send(self, connexion: AbstractProtocol):
        pass

    def receive(self, connexion: AbstractProtocol):
        self._data = connexion.read_line()

    def process(self):
        """ Processes the command """
        logger.debug('> start command: %s', str(self))
        if self._data:
            logger.info('## DEBUG command: Received data: %s ##', self._data)
        logger.debug('> command done: %s', str(self))
