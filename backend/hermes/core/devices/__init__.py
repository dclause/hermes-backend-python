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
from typing import final

from hermes.core.commands import CommandCode
from hermes.core.plugins import AbstractPlugin
from hermes.core.struct import MetaPluginType


class DeviceType(IntEnum):
    """ Defines the device codes that are known by the application.

    Each device code will be cast to a 8bits integer, therefore at most 255 commands can be interpreted.

    Device codes cannot be edited later in time for compatibility purposes. Therefore, the list below may be unsorted as
    time goes on and new device codes are added.
    """

    LED = 1
    SERVO = 2


class AbstractDevice(AbstractPlugin, metaclass=MetaPluginType):
    """ Manages plugins of type devices. """

    # @todo Remove all entry parameters. Add a hydrate() method.
    def __init__(self, board: int, name: str = "", actions=None, inputs=None):
        super().__init__()
        if actions is None:
            actions = []
        if inputs is None:
            inputs = []
        self.name = name
        self.board: int = board
        self.actions = actions
        self.inputs = inputs

    @abstractmethod
    def _to_bytes(self) -> bytearray:
        """
        Returns the bytearray representation of the device necessary to rebuild the device on the robot side.

        The PATCH command (@see commands/patch.py) will create a unified header for a device (code, id), hence this
        method should exclude those. (@see devices/led.py for a simple example).

        Returns:
            bytearray
        """
        return bytearray()

    @final
    def to_bytes(self) -> bytearray:
        """
        Exposed version of '_to_bytes()' method.
        @see _to_bytes()

        The purpose is to make sure every single bytearray representation of a device has the same format :
            - empty of no internal data to expose.
            - CommandCode.PATCH | type | id | <internal _to_bytes() representation | CommandCode.END_OF_LINE
        """
        internal_to_bytes: bytearray = self._to_bytes()
        if len(internal_to_bytes):
            return bytearray([CommandCode.PATCH, self.type.value, self.id]) + \
                   internal_to_bytes + \
                   bytearray([CommandCode.END_OF_LINE])
        return bytearray()


__ALL__ = ["AbstractDevice", "DeviceType"]
