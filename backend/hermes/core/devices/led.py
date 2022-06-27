"""
LED device: this device represents a simple LED.
https://en.wikipedia.org/wiki/Light-emitting_diode
"""

from hermes.core.devices import AbstractDevice, tag


@tag('!LED')
class LedDevice(AbstractDevice):
    """ LED class """

    def __init__(self, name: str, pin: int, default: bool):
        super().__init__(name)
        self.pin = pin
        self.default = default
        self.value = default

    def __repr__(self):
        return f"{self.__class__.__name__,}(" \
               f"name={self.name}, " \
               f"pin={self.pin}, " \
               f"default={self.default}, " \
               f"value={self.value})"
