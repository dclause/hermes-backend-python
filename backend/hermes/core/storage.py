"""
Defines the storage interface used to load/dump configs. It currently uses YAML 1.2 via the ruamel.yaml.

The purpose to separate it to its own module is to later be able to swap to a different dumper style if needed.
"""
import glob
import io
import os.path
from typing import Any

import ruamel.yaml
from mergedeep import merge

from hermes.core import logger
from hermes.core.boards import AbstractBoard
from hermes.core.boards.arduino import StringEnum
from hermes.core.devices import AbstractDevice
from hermes.core.helpers import ROOT_DIR

_storage = ruamel.yaml.YAML(typ='safe')


class StorageNamespace(StringEnum):
    """ Defines the existing namespace within the application. """
    CORE = os.path.join('core', 'configs')  # Any configuration provided by core.
    MODULE = os.path.join('modules', 'configs')  # Any configuration provided by a module.
    PROFILE = 'configs'  # Any configuration from the active profile.


class StorageType(StringEnum):
    """ Defines the existing configuration types within the application. """
    GLOBAL = 'global'  # Configurations relative to the application itself (port, host, ...)
    PROFILE = 'profile'  # Configurations relative to the application itself (port, host, ...)
    BOARD = 'boards'  # Configurations relative to boards within the robot (arduino, ...)
    DEVICE = 'devices'  # Configurations relative to devices connected to the boards (led, servo, ...)


def init():
    """ Init the YAML loader/dumper. """
    logger.info(' > Init storage')

    # Register boards.
    for board_type in AbstractBoard.plugins:
        _storage.register_class(board_type)

    # Register devices.
    for device_type in AbstractDevice.plugins:
        _storage.register_class(device_type)


def read(namespace: StorageNamespace, config_type: StorageType) -> dict:
    """
    Reads the given config type from the given namespace.

    Args:
        namespace (StorageNamespace):
            The namespace within the hermes application where the configuration is expected.
        config_type (StorageType):
            The configuration type.

    Returns:
       List(str, Any): A list of configurations
    """
    configs = {}

    # Find all files corresponding to the config_type for the given namespace.
    filenames = glob.glob(os.path.join(ROOT_DIR, namespace, '**', f'{config_type}.yml'), recursive=True)
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as file:
            if config_type is StorageType.GLOBAL or config_type is StorageType.PROFILE:
                data = _storage.load(file)
                configs = merge(configs, data)
            else:
                data = {}
                plugins = _storage.load_all(file)
                for plugin in plugins:
                    data[plugin.id] = plugin
                configs = {**configs, **data}

    return configs


def write(config_type: StorageType, data: Any) -> None:
    """
    Stores the given config data to the active profile.

    Args:
        config_type (StorageType):
            The configuration type.
        data (Any):
            The data to store.
    """
    filename = os.path.join(ROOT_DIR, StorageNamespace.PROFILE, f'{config_type}.yml')
    with open(filename, 'w', encoding='utf-8') as file:
        if config_type is StorageType.GLOBAL:
            _storage.dump(data, file)
        else:
            _storage.dump_all(data, file)


def dump(data) -> Any:
    """
    Returns the given data dump.

    Args:
        data (Any):
            The data to dump.
    """
    buffer = io.StringIO()
    _storage.dump(data, buffer)
    return buffer.getvalue()
