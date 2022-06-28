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

from hermes import __version__


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

    _args = vars(parser.parse_args())
    logzero.logger.debug(_args)
    return _args


# @todo implement this method
def _get_plugins_config() -> dict[str, Any]:
    """
    Build configuration object from plugins YAML files.

    Returns:
        List(str, object): A list of argument
    """
    return {}


# @todo implement this method
def _get_core_config() -> dict[str, Any]:
    """
    Build configuration object from core YAML files.

    Returns:
        List(str, object): A list of argument
    """
    return {}


# @todo implement this method
def _get_default_config() -> dict[str, Any]:
    """
    Build configuration object from default configuration that is built-in the application.

    Returns:
        List(str, object): A list of argument
    """
    return {
        # Defines the number of orders that can be received / sent at a time to a board.
        'semaphore': 5,
    }


# Globally available CONFIG object.
CONFIG: dict[str, Any] = {
    'STATE': {},  # Stores the current application state as a whole @todo evaluate if necessary when devices are done.
}


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

    # Add a specific dumper for string (to be surrounded by quotes)
    # DataDumper.add_representer(str, _quoted_presenter)
    # devices.init()
    # boards.init()

    global CONFIG
    CONFIG = {**_get_cmd_config(), **_get_plugins_config(), **_get_core_config()}


__ALL__ = ["CONFIG", "init"]
