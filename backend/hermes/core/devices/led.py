"""
LED device: this device represents a simple LED.
https://en.wikipedia.org/wiki/Light-emitting_diode
"""
from hermes.core.devices import AbstractDevice, DeviceCode


class LedDevice(AbstractDevice):
    """ LED class """

    # @todo should PIN(s) be abstracted to a dict ?
    def __init__(self, code: DeviceCode, name: str, board: int, default: bool, pin: int):
        super().__init__(code, name, board, default)
        self.pin: int = pin

    def to_bytes(self) -> bytearray:
        return bytearray([self.pin, self.default])
