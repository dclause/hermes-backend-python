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
import collections.abc
from typing import Any

import logzero
from mergedeep import merge

from hermes import __version__
from hermes.core import storage
from hermes.core.storage import StorageNamespace, StorageType


def _get_cmd_config() -> dict[str, Any]:
    """
    Build configuration object from commandline parameters.

    Returns:
        List(str, object): A list of argument
    """
    parser = argparse.ArgumentParser()

    # Optional PORT number argument (eg. -p 9999)
    parser.add_argument('-p', '--port', action='store', dest='port', default=9999, help='PORT number for the GUI')

    # Optional WEBGUI boolean argument (eg. -w)
    parser.add_argument('-w', '--webGUI', action='store_true', dest='webGUI', help='Starts serving the GUI')

    # Specify output of "--version"
    parser.add_argument('--version', action='version', version=f'RMS version {__version__}')

    cmdline_args = vars(parser.parse_args())
    config = {
        'web': {
            'enabled': cmdline_args['webGUI'],
            'port': cmdline_args['port']
        }
    }

    logzero.logger.debug('> Read configuration from cmdline:')
    logzero.logger.debug(config)
    return config


# @todo implement this method
def _get_module_config() -> dict[str, Any]:
    """
    Build configuration object from modules YAML files.

    Returns:
        List(str, object): A list of argument
    """
    return {}


# @todo implement this method
def _get_profile_config() -> dict[str, Any]:
    """
    Build configuration object from profile YAML files.

    Returns:
        List(str, object): A list of argument
    """
    return {}


def _get_core_config() -> dict[str, Any]:
    """
    Build configuration object from core YAML files.

    Returns:
        List(str, object): A list of argument
    """
    config = storage.read(StorageNamespace.CORE, StorageType.GLOBAL)
    logzero.logger.debug('> Read configuration from core:')
    logzero.logger.debug(config)
    return config


# Globally available CONFIG object.
CONFIG: dict[str, Any] = {}


# @todo rework when needs get better defined
def update(new_values):
    """ Patches the GLOBAL states with given values. """
    for key, value in new_values.items():
        if isinstance(value, collections.abc.Mapping):
            CONFIG[key] = new_values(CONFIG.get(key, {}), value)
        else:
            CONFIG[key] = value
    return CONFIG


def _quoted_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')


def init():
    """
    Initializes the global CONFIG Object.

    By order of importance, the configurations are :
        - extracted from commandline data
        - extracted from plugins config YAMLs
        - extracted from core YAMLs
    """
    print(' > Loading config')

    # pylint: disable-next=global-statement
    global CONFIG
    CONFIG = merge(_get_core_config(), _get_cmd_config(), _get_module_config(), _get_profile_config())
    logzero.logger.debug('> Total build configuration:')
    logzero.logger.debug(CONFIG)


__ALL__ = ["CONFIG", "init"]
