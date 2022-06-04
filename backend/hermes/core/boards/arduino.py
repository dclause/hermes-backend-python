"""
Represents a connexion to an electronic board (arduino-like) by embedding its pyserial connexion.
"""

from hermes.core.boards import AbstractBoard


class ArduinoBoard(AbstractBoard):
    """ ArduinoBoard implementation """
