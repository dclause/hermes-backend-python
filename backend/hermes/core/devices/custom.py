"""
Custom device:

Represents a generic device that is not explicitly supported as a type by the application, yet that is built from the
configuration generic enough to be implemented here and  handle by the system.
"""

from hermes.core.devices import AbstractDevice


class CustomDevice(AbstractDevice):
    """ Custom Device class """

    def _to_bytes(self) -> bytearray:
        return bytearray()
