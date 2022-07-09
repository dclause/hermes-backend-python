"""
LED device: this device represents a simple LED.
https://en.wikipedia.org/wiki/Light-emitting_diode
"""
from hermes.core.devices import AbstractDevice


class LedDevice(AbstractDevice):
    """ LED class """

    # @todo should PIN(s) be abstracted to a dict ?
    def __init__(self, name: str, board: int, default: bool, pin: int):
        super().__init__(name, board, default)
        self.pin: int = pin
