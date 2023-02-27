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
from hermes.core.helpers import ROOT_DIR
from hermes.core.plugins import AbstractPlugin
from hermes.core.struct import StringEnum

_storage = ruamel.yaml.YAML(typ='safe')
_storage.sort_base_mapping_type_on_output = False


class StorageNamespace(StringEnum):
    """ Defines the existing namespace within the application. """
    CORE = os.path.join('configs')  # Any configuration provided by core.
    MODULE = os.path.join('modules', 'configs')  # Any configuration provided by a module.
    PROFILE = os.path.join('..', 'configs')  # Any configuration from the active profile.


class StorageType(StringEnum):
    """ Defines the existing configuration types within the application. """
    GLOBAL = 'global'  # Configurations relative to the application itself (port, host, ...)
    PROFILE = 'profile'  # Configurations relative to the application itself (port, host, ...)
    BOARD = 'boards'  # Configurations relative to boards within the robot (arduino, ...)
    DEVICE = 'devices'  # Configurations relative to devices connected to the boards (led, servo, ...)


def init():
    """ Init the YAML loader/dumper. """
    logger.info(' > Init storage')

    # @todo fixme: 'plugins' here only does not fail by convention.
    for class_type in AbstractPlugin.__subclasses__():
        for plugin in class_type.plugins:
            _storage.register_class(plugin)


def load() -> dict[str, Any]:
    """
    Load all available configurations and merge/concatenate it accordingly
    Returns:
       List(str, Any): A list of configurations
    """
    config: dict[str, Any] = {}
    for namespace in StorageNamespace:
        # Find all files corresponding to the config_type for the given namespace.
        filenames = glob.glob(os.path.join(ROOT_DIR, namespace, '*.yml'), recursive=False)
        for filename in filenames:
            plugin_name = os.path.basename(filename)[:-4]
            with open(filename, 'r', encoding='utf-8') as file:
                if plugin_name not in config:
                    config[plugin_name] = {}
                data = _storage.load_all(file)
                for plugin in data:
                    if isinstance(plugin, dict):
                        config[plugin_name] = merge({}, config[plugin_name], plugin)
                    elif isinstance(plugin, list):
                        data = {}
                        for index, item in enumerate(plugin):
                            if 'id' in item:
                                index = item['id']
                            data[index] = item
                        config[plugin_name] = {**config[plugin_name], **data}
                    else:
                        data = {plugin.id: plugin}
                        config[plugin_name] = {**config[plugin_name], **data}
    return config


def write(config_type: StorageType, data: Any) -> None:
    """
    Stores the given config data to the active profile.

    Args:
        config_type (StorageType):
            The configuration type.
        data (Any):
            The data to store.
    """
    filename = os.path.join(CONFIG_DIR, StorageNamespace.PROFILE, f'{config_type}.yml')
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
