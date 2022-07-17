"""
LED device: this device represents a simple LED.
https://en.wikipedia.org/wiki/Light-emitting_diode
"""

from hermes.core.devices import AbstractDevice, DeviceType


class LedDevice(AbstractDevice):
    """ LED class """

    @property
    def __type__(self) -> DeviceType:
        return DeviceType.LED

    def _to_bytes(self) -> bytearray:
        return bytearray()
