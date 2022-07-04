"""
LED device: this device represents a simple LED.
https://en.wikipedia.org/wiki/Light-emitting_diode
"""
from hermes.core.boards import AbstractBoard
from hermes.core.devices import AbstractDevice


class LedDevice(AbstractDevice):
    """ LED class """

    def __init__(self, name: str, board: AbstractBoard, pin: int, default: bool):
        super().__init__(name)
        self.pin: int = pin
        self.board: AbstractBoard = board
        self.default: bool = default
        self.value: bool = default
