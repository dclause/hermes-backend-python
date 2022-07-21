"""
Represents a connexion to an electronic board (arduino-like) by embedding its pyserial connexion.
"""

from hermes.core.boards import AbstractBoard
from hermes.core.protocols import AbstractProtocol
from hermes.core.struct import StringEnum


class ArduinoBoardType(StringEnum):
    """ Defines the arduino board types. """
    NANO = 'NANO'
    UNO = 'UNO'
    MEGA = 'MEGA'


class ArduinoBoard(AbstractBoard):
    """ ArduinoBoard implementation """

    def __init__(self, protocol: AbstractProtocol, model: ArduinoBoardType):
        self.model: ArduinoBoardType = model
        super().__init__(protocol)
