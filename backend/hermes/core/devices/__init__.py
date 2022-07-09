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

from hermes.core.plugins import AbstractPlugin
from hermes.core.struct import MetaPluginType


class AbstractDevice(AbstractPlugin, metaclass=MetaPluginType):
    """ Manages plugins of type devices. """

    def __init__(self, name: str, board: int, default: any):
        super().__init__(name)
        self.board: int = board
        self.default: any = default
        self.state: any = default


__ALL__ = ["AbstractDevice"]
