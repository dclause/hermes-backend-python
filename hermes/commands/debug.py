"""
DEBUG Command: Displays debug data send from slave board.

code: MessageCode::DEBUG
"""

from hermes.commands import AbstractCommand
from hermes.core import logger
from hermes.core.dictionary import MessageCode
from hermes.protocols import AbstractProtocol


class DebugCommand(AbstractCommand):
    """ Displays debug data send from slave board. """

    def __init__(self):
        super().__init__()
        self._data = ""

    @property
    def code(self) -> MessageCode:
        return MessageCode.DEBUG

    def receive(self, connexion: AbstractProtocol):
        self._data = connexion.read_line()

    def process(self):
        """ Processes the command. """
        logger.info(f'## DEBUG ROBOT: {self._data} ##')
