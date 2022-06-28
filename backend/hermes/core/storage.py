"""
Defines the storage interface used to load/dump configs. It currently uses YAML 1.2 via the ruamel.yaml.

The purpose to separate it to its own module is to later be able to swap to a different dumper style if needed.
"""

import ruamel.yaml

from hermes.core.boards import AbstractBoard
from hermes.core.devices import AbstractDevice

storage = ruamel.yaml.YAML()


def init():
    """ Init the YAML loader/dumper. """
    print(' > Init storage')

    # Register boards.
    for board_type in AbstractBoard.plugins:
        storage.register_class(board_type)

    # Register devices.
    for device_type in AbstractDevice.plugins:
        storage.register_class(device_type)
