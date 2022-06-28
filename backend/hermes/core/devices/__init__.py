""" Devices package """

import yaml

from hermes.core.plugins import AbstractPlugin, tag
from hermes.core.struct import MetaPluginType


class DataLoader(yaml.SafeLoader):
    """
    Extends SafeLoader
    @see init() method.
    """


class DataDumper(yaml.SafeDumper):
    """
    Extends SafeDumper.
    @see init() method.
    """


@tag('!Device')
class AbstractDevice(AbstractPlugin, metaclass=MetaPluginType):
    """ Manages plugins of type devices. """


def init():
    """ Registers all devices with the proper YAML loader/representer. """
    print("     - Register devices")
    for device in AbstractDevice.plugins:
        # Registers custom tag in the loader to safely load the yaml to Device object.
        DataLoader.add_constructor(device.TAG, device.from_yaml)
        # Registers the method to serialize the object to yaml using the appropriate method.
        DataDumper.add_representer(device, device.to_yaml)


__ALL__ = ["AbstractDevice", "DataLoader", "DataDumper", "init"]
