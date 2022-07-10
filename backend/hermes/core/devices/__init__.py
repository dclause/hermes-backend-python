"""
Devices package.
This package contains all implemented devices provided by default in HERMES.

A device is a physical piece of electronic wired to a Board (ex: led, servo, etc...).
@see Board definition in boards package.

A device state is mutable via commands (@see Command definition in commands package).
The commands can be sent via the 'command' socketIO method.
@see Server definition in server.py.
@see Command definition in commands package.

Devices can be created from configs file leaving in the config/devices.yml file. Each device must validate the
schema provided within this package.
Devices are detected when the package is imported for the first time and globally available via the CONFIG under
the `devices` key
"""
from abc import abstractmethod
from enum import IntEnum

from hermes.core.plugins import AbstractPlugin
from hermes.core.struct import MetaPluginType


class DeviceCode(IntEnum):
    """ Defines the device codes that are known by the application.

    Each device code will be cast to a 8bits integer, therefore at most 255 commands can be interpreted.

    Device codes cannot be edited later in time for compatibility purposes. Therefore, the list below may be unsorted as
    time goes on and new device codes are added.
    """

    LED = 1
    SERVO = 1


class AbstractDevice(AbstractPlugin, metaclass=MetaPluginType):
    """ Manages plugins of type devices. """

    def __init__(self, code: DeviceCode, name: str, board: int, default: any):
        super().__init__(name)
        self.code: DeviceCode = code
        self.board: int = board
        self.default: any = default
        self.state: any = default

    @abstractmethod
    def to_bytes(self) -> bytearray:
        """
        Returns the bytearray representation of the device necessary to rebuild the device on the robot side.

        The PATCH command (@see commands/patch.py) will create a unified header for a device (code, id), hence this
        method should exclude those. (@see devices/led.py for a simple example).

        Returns:
            bytearray
        """
        pass


__ALL__ = ["AbstractDevice", "DeviceCode"]
