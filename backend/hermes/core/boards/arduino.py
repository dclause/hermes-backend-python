"""
Represents a connexion to an electronic board (arduino-like) by embedding its pyserial connexion.
"""

from hermes.core.boards import AbstractBoard
from hermes.core.protocols.usbserial import SerialProtocol
from hermes.core.struct import StringEnum


class ArduinoBoardType(StringEnum):
    """ Defines the arduino board types. """
    NANO = 'NANO'
    UNO = 'UNO'
    MEGA = 'MEGA'


class ArduinoBoard(AbstractBoard):
    """ ArduinoBoard implementation """

    def __init__(self, port: str):
        self.port = port
        self.model: ArduinoBoardType = ArduinoBoardType.MEGA
        super().__init__(SerialProtocol(self.port))
