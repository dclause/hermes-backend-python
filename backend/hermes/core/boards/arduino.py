"""
Represents a connexion to an electronic board (arduino-like) by embedding its pyserial connexion.
"""

from hermes.core.boards import AbstractBoard
from hermes.core.protocols import AbstractProtocol
from hermes.core.protocols.usbserial import SerialProtocol
from hermes.core.struct import StringEnum


class ArduinoBoardType(StringEnum):
    """ Defines the arduino board types. """
    NANO = 'NANO'
    UNO = 'UNO'
    MEGA = 'MEGA'


class ArduinoBoard(AbstractBoard):
    """ ArduinoBoard implementation """

    def __init__(self, name, port: str, model: ArduinoBoardType):
        self.port = port
        self.model = model
        connexion: AbstractProtocol = SerialProtocol(self.port)
        super().__init__(name, connexion)
