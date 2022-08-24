"""
LED device: this device represents a simple LED.
https://en.wikipedia.org/wiki/Light-emitting_diode
"""

from hermes.core.devices.boolean import BooleanOutputDevice


class LedDevice(BooleanOutputDevice):
    """ LED class """
