"""
LED device: this device represents a simple LED.
https://en.wikipedia.org/wiki/Light-emitting_diode
"""

from hermes.core.devices import AbstractDevice


class LedDevice(AbstractDevice):
    """ LED class """

    def _to_bytes(self) -> bytearray:
        return bytearray()
