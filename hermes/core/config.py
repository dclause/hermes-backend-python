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
from typing import Any, MutableMapping, Dict

from mergedeep import merge

from hermes import __version__
from hermes.core import storage, logger
from hermes.core.struct import MetaSingleton


class Config(metaclass=MetaSingleton):
    """ Global config object """
    __config: Dict[str, Any] = {}

    @staticmethod
    def init():
        """
        Initializes global config objects.

        By order of importance, the configurations are :
            - extracted from commandline data
            - extracted from plugins config YAMLs
            - extracted from core YAMLs
        """
        logger.info(' > Loading config')

        # @todo rename: why load storage here ?
        Config.__config = storage.load()
        merge(Config.__config['global'], _get_cmd_config())

        logger.debug('> Total build configuration:')
        logger.debug(Config.__config)

    @staticmethod
    def get(name: str) -> dict[str, Any]:
        """ Gets a configuration object. """
        if name in Config.__config:
            return Config.__config[name]
        raise NameError(f"Configuration of type {name} not accepted in get() method")

    @staticmethod
    def set(name: str, value: Any) -> None:
        """ Sets a configuration object. """
        if name in Config.__config:
            Config.__config[name] = value
        else:
            raise NameError(f"Configuration of type {name} not accepted in set() method")


def _get_cmd_config() -> MutableMapping:
    """
    Build configuration object from commandline parameters.

    Returns:
        MutableMapping: A list of configurations
    """
    parser = argparse.ArgumentParser()

    # Optional PORT number argument (eg. -p 9999)
    parser.add_argument('-p', '--port', action='store', dest='port', default=9999, help='PORT number for the GUI')

    # Optional open UI argument (eg. --open)
    parser.add_argument('--open', action='store_true', dest='webGUI', help='Opens the UI in a browser on startup')

    # Optional debug argument (eg. --debug)
    parser.add_argument('--debug', action='store_true', dest='debug')

    # Optional version argument (eg. --debug)
    parser.add_argument('--version', action='version', version=f'RMS version {__version__}')

    cmdline_args = vars(parser.parse_args())
    configuration = {
        'web': {
            'enabled': cmdline_args['webGUI'],
        },
        'server': {
            'port': cmdline_args['port']
        }
    }

    if cmdline_args['debug']:
        logger.loglevel(logger.DEBUG)

    logger.debug('> Read configuration from cmdline:')
    logger.debug(configuration)
    return configuration


CONFIG = Config()

__ALL__ = ['CONFIG']
