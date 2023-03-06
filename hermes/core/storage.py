"""
Defines the storage interface used to load/dump configs. It currently uses YAML 1.2 via the ruamel.yaml.

The purpose to separate it to its own module is to later be able to swap to a different dumper style if needed.
"""
import io
from pathlib import Path
from typing import Any

import ruamel.yaml
from mergedeep import merge

from hermes.core import logger
from hermes.core.helpers import CONFIG_DIR, ROOT_DIR
from hermes.core.plugins import AbstractPlugin
from hermes.core.struct import StringEnum

_storage = ruamel.yaml.YAML(typ='safe')
_storage.sort_base_mapping_type_on_output = False  # type: ignore[assignment]


class StorageType(StringEnum):
    """Defines the existing configuration types within the application."""

    GLOBAL = 'global'  # Configurations relative to the application itself (port, host, ...)
    PROFILE = 'profile'  # Configurations relative to the application itself (port, host, ...)
    BOARD = 'boards'  # Configurations relative to boards within the robot (arduino, ...)
    DEVICE = 'devices'  # Configurations relative to devices connected to the boards (led, servo, ...)


def init() -> None:
    """Init the YAML loader/dumper."""
    logger.info(' > Init storage')

    # This is needed for storage to know about the storable classes.
    # and register them.
    # The classes should first be imported which is the job of plugin handler.
    # @see plugin.init().
    for plugin_type in AbstractPlugin.types():
        if hasattr(plugin_type, 'plugins'):
            for plugin in plugin_type.plugins:
                _storage.register_class(plugin)


def load() -> dict[str, Any]:
    """
    Load all available configurations and merge/concatenate it accordingly
    Returns:
       List(str, Any): A list of configurations.
    """
    config: dict[str, Any] = {}

    for scope in ['', 'hermes', 'modules']:  # @todo also load properly from modules
        loadable_config_files = Path(ROOT_DIR, scope, 'configs').glob('*.yml')
        for filename in loadable_config_files:
            plugin_name = filename.name[:-4]
            with filename.open(encoding='utf-8') as file:
                if plugin_name not in config:
                    config[plugin_name] = {}
                data = _storage.load_all(file)
                for plugin in data:
                    if isinstance(plugin, dict):
                        config[plugin_name] = merge({}, config[plugin_name], plugin)
                    elif isinstance(plugin, list):
                        data = {}
                        for index, item in enumerate(plugin):
                            key = item['id'] if 'id' in item else index
                            data[key] = item
                        config[plugin_name] = {**config[plugin_name], **data}
                    else:
                        data = {plugin.id: plugin}
                        config[plugin_name] = {**config[plugin_name], **data}
    return config


def write(config_type: StorageType, data: Any) -> None:
    """
    Store the given config data to the active profile.

    :param StorageType config_type: The configuration type.
    :param Any data: The data to store.
    """
    filename = Path(CONFIG_DIR, f'{config_type}.yml')
    with filename.open(mode='w', encoding='utf-8') as file:
        if config_type is StorageType.GLOBAL:
            _storage.dump(data, file)
        else:
            _storage.dump_all(data, file)


# @todo evaluate when storage will write configs.
def dump(data: Any) -> Any:
    """
    Dump the given data dump.

    :param any data: The data to dump.
    """
    buffer = io.StringIO()
    _storage.dump(data, buffer)
    return buffer.getvalue()
