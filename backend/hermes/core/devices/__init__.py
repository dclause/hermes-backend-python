""" Devices package """

from hermes.core.plugins import AbstractPlugin
from hermes.core.struct import MetaPluginType


class AbstractDevice(AbstractPlugin, metaclass=MetaPluginType):
    """ Manages plugins of type devices. """


__ALL__ = ["AbstractDevice", "DataLoader", "DataDumper"]
