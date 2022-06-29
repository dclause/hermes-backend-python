"""
Configuration module.

Handles the configuration for the application. The configurations are stored in YAML files in a `config` package of a
given "space".
 - Default space is in `core` package and is given by the application itself
 - Plugins living in the `plugins` space can each have a `config` package overriding the configuration.
 - Finally the upmost specific configuration is the one given as parameters of the commandline when starting the
  application.
"""

import argparse
from typing import Any, MutableMapping

from mergedeep import merge, Strategy

from hermes import __version__
from hermes.core import storage, logger
from hermes.core.boards import AbstractBoard
from hermes.core.devices import AbstractDevice
from hermes.core.storage import StorageNamespace, StorageType

# Use global objects to be filled during config reading (@see _get_module_config, _get_profile_config)
# The reason is those cannot be merged (and are not mergeable) as a config can be.
# Device list is more 'concatenated' than merged in the proper way.
_global = {}
_profile = {}
_devices = {}
_boards = {}


def _get_cmd_config() -> MutableMapping:
    """
    Build configuration object from commandline parameters.

    Returns:
        MutableMapping: A list of configurations
    """
    parser = argparse.ArgumentParser()

    # Optional PORT number argument (eg. -p 9999)
    parser.add_argument('-p', '--port', action='store', dest='port', default=9999, help='PORT number for the GUI')

    # Optional WEBGUI boolean argument (eg. -w)
    parser.add_argument('-w', '--webGUI', action='store_true', dest='webGUI', help='Starts serving the GUI')

    # Specify output of "--version"
    parser.add_argument('--version', action='version', version=f'RMS version {__version__}')

    cmdline_args = vars(parser.parse_args())
    configuration = merge(_get_default_config(), {
        StorageType.GLOBAL: {
            'web': {
                'enabled': cmdline_args['webGUI'],
            },
            'server': {
                'port': cmdline_args['port']
            }
        }
    })

    logger.debug('> Read configuration from cmdline:')
    logger.debug(configuration)
    return configuration


def _get_modules_config() -> MutableMapping:
    """
    Build configuration object from modules YAML files.

    Returns:
        MutableMapping: A list of configurations
    """
    configuration = _get_default_config()

    # Read global configuration from modules.
    config = {StorageType.GLOBAL: storage.read(StorageNamespace.MODULE, StorageType.GLOBAL)}
    configuration = merge(configuration, config)

    # Read profile specific configuration from modules.
    profile = {StorageType.PROFILE: storage.read(StorageNamespace.MODULE, StorageType.PROFILE)}
    configuration = merge(configuration, profile)

    # Read boards from modules.
    boards = {StorageType.BOARD: storage.read(StorageNamespace.MODULE, StorageType.BOARD)}
    configuration = merge(configuration, boards, strategy=Strategy.ADDITIVE)

    # Read devices from modules.
    devices = {StorageType.DEVICE: storage.read(StorageNamespace.MODULE, StorageType.DEVICE)}
    configuration = merge(configuration, devices, strategy=Strategy.ADDITIVE)

    logger.debug('> Read configuration from modules:')
    logger.debug(configuration)
    return configuration


def _get_profile_config() -> MutableMapping:
    """
    Build configuration object from profile YAML files.

    Returns:
        MutableMapping: A list of configurations
    """
    configuration = _get_default_config()

    # Read global configuration in the profile.
    config = {StorageType.GLOBAL: storage.read(StorageNamespace.PROFILE, StorageType.GLOBAL)}
    configuration = merge(configuration, config)

    # Read profile specific configuration in the profile.
    profile = {StorageType.PROFILE: storage.read(StorageNamespace.PROFILE, StorageType.PROFILE)}
    configuration = merge(configuration, profile)

    # Read boards from the profile
    boards = {StorageType.BOARD: storage.read(StorageNamespace.PROFILE, StorageType.BOARD)}
    configuration = {**configuration, **boards}  # merge(configuration, boards, strategy=Strategy.ADDITIVE)

    # Read devices from the profile
    devices = {StorageType.DEVICE: storage.read(StorageNamespace.PROFILE, StorageType.DEVICE)}
    configuration = {**configuration, **devices}  # merge(configuration, devices, strategy=Strategy.ADDITIVE)

    logger.debug('> Read configuration from profile:')
    logger.debug(configuration)
    return configuration


def _get_core_config() -> MutableMapping:
    """
    Build configuration object from core YAML files.

    Returns:
        MutableMapping: A list of configurations
    """
    configuration = _get_default_config()

    # Read global configuration from core.
    config = {StorageType.GLOBAL: storage.read(StorageNamespace.CORE, StorageType.GLOBAL)}
    configuration = merge(configuration, config)

    logger.debug('> Read configuration from core:')
    logger.debug(configuration)
    return configuration


def _get_default_config() -> MutableMapping:
    """
    Builds the bar minimal empty config object.

    Returns:
        MutableMapping: A list of configurations
    """
    return {
        StorageType.GLOBAL: {},
        StorageType.PROFILE: {},
        StorageType.BOARD: {},
        StorageType.DEVICE: {}
    }


# Globally available config objects.
GLOBAL: dict[str, Any] = {}
PROFILE: dict[str, Any] = {}
BOARDS: dict[int, AbstractBoard] = {}
DEVICES: dict[int, AbstractDevice] = {}


# @todo rework when needs get better defined
# def update(new_values):
#     """ Patches the GLOBAL states with given values. """
#     for key, value in new_values.items():
#         if isinstance(value, collections.abc.Mapping):
#             CONFIG[key] = new_values(CONFIG.get(key, {}), value)
#         else:
#             CONFIG[key] = value
#     return CONFIG


def init():
    """
    Initializes global config objects.

    By order of importance, the configurations are :
        - extracted from commandline data
        - extracted from plugins config YAMLs
        - extracted from core YAMLs
    """
    logger.info(' > Loading config')

    default_config = _get_default_config()
    core_config = _get_core_config()
    modules_config = _get_modules_config()
    profile_config = _get_profile_config()
    cmd_config = _get_cmd_config()

    ########################
    # Merge global config.

    # pylint: disable-next=global-statement
    global GLOBAL
    GLOBAL = merge(
        default_config[StorageType.GLOBAL],
        core_config[StorageType.GLOBAL],
        modules_config[StorageType.GLOBAL],
        profile_config[StorageType.GLOBAL],
        cmd_config[StorageType.GLOBAL]
    )

    ########################
    # Merge profile config.

    # pylint: disable-next=global-statement
    global PROFILE
    PROFILE = merge(
        default_config[StorageType.PROFILE],
        core_config[StorageType.PROFILE],
        modules_config[StorageType.PROFILE],
        profile_config[StorageType.PROFILE],
        cmd_config[StorageType.PROFILE]
    )

    ########################
    # Concatenate boards.

    # pylint: disable-next=global-statement
    global BOARDS
    BOARDS = {
        **default_config[StorageType.BOARD],
        **core_config[StorageType.BOARD],
        **modules_config[StorageType.BOARD],
        **profile_config[StorageType.BOARD],
        **cmd_config[StorageType.BOARD]
    }

    ########################
    # Concatenate devices.

    # pylint: disable-next=global-statement
    global DEVICES
    DEVICES = {
        **default_config[StorageType.DEVICE],
        **core_config[StorageType.DEVICE],
        **modules_config[StorageType.DEVICE],
        **profile_config[StorageType.DEVICE],
        **cmd_config[StorageType.DEVICE]
    }

    logger.debug('> Total build configuration:')
    logger.debug(GLOBAL)
    logger.debug(PROFILE)
    logger.debug(BOARDS)
    logger.debug(DEVICES)


__ALL__ = ['GLOBAL', 'PROFILE', 'BOARDS', 'DEVICES', 'init']
