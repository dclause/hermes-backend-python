""" Devices package """

import yaml

# pylint: disable-next=too-many-ancestors
from hermes.core.plugins import AbstractPlugin, tag


# pylint: disable-next=too-many-ancestors
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
class AbstractDevice(AbstractPlugin):
    """ Manages plugins of type devices. """

    def __str__(self):
        return f'Device {self.name}'


__ALL__ = ["AbstractDevice", "DataLoader", "DataDumper"]


def init():
    """ Registers all devices with the proper YAML loader/representer. """
    for device in AbstractDevice.plugins:
        # Registers custom tag in the loader to safely load the yaml to Device object.
        DataLoader.add_constructor(device.TAG, device.from_yaml)
        # Registers the method to serialize the object to yaml using the appropriate method.
        DataDumper.add_representer(device, device.to_yaml)
