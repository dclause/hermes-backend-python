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

    # Optional API start option + port / host configurations
    api_group = parser.add_argument_group('Websocket API')
    api_group.add_argument('--api', action='store_true', dest='api', help='Starts the websocket API server.')
    api_group.add_argument('-ah', '--api-host', action='store', dest='api-port', default=argparse.SUPPRESS,
                           help='API host configuration')
    api_group.add_argument('-ap', '--api-port', action='store', dest='api-host', default=argparse.SUPPRESS,
                           help='API port configuration')
    api_group.add_argument('-ar', '--api-reload', action='store_true', dest='api-reload', default=argparse.SUPPRESS,
                           help='API auto-reload when file changes')

    # Optional UI start option + port / host configurations
    ui_group = parser.add_argument_group('Frontend UI')
    ui_group.add_argument('--ui', action='store_true', dest='ui', help='Starts the UI server.')
    ui_group.add_argument('-uo', '--ui-open', action='store_true', dest='ui-open', default=argparse.SUPPRESS,
                          help='Open the UI in browser on startup (needs --ui enabled).')
    ui_group.add_argument('-ur', '--ui-reload', action='store_true', dest='ui-reload', default=argparse.SUPPRESS,
                          help='UI auto-reload when file changes')
    ui_group.add_argument('-uh', '--ui-host', action='store', dest='ui-port', default=argparse.SUPPRESS,
                          help='Frontend UI host configuration')
    ui_group.add_argument('-up', '--ui-port', action='store', dest='ui-host', default=argparse.SUPPRESS,
                          help='Frontend UI port configuration')

    # Optional debug argument (eg. --debug)
    parser.add_argument('--debug', action='store_true', dest='debug')

    # Optional version argument (eg. --debug)
    parser.add_argument('--version',
                        action='version',
                        default=argparse.SUPPRESS,
                        version=f'HERMES version {__version__}')

    cmdline_args = vars(parser.parse_args())
    configuration = {}

    # Add ui configuration overrides.
    if cmdline_args['ui']:
        configuration['ui'] = {'enabled': True}
        if 'ui-open' in cmdline_args:
            configuration['ui']['open'] = True
        if 'ui-host' in cmdline_args:
            configuration['ui']['host'] = cmdline_args['ui-host']
        if 'ui-port' in cmdline_args:
            configuration['ui']['port'] = cmdline_args['ui-port']
        if 'ui-reload' in cmdline_args:
            configuration['ui']['reload'] = True

    # Add api configuration overrides.
    if cmdline_args['api']:
        configuration['api'] = {'enabled': True}
        if 'api-host' in cmdline_args:
            configuration['api']['host'] = cmdline_args['api-host']
        if 'api-port' in cmdline_args:
            configuration['api']['port'] = cmdline_args['api-port']
        if 'api-reload' in cmdline_args:
            configuration['api']['reload'] = True

    if cmdline_args['debug']:
        configuration['debug'] = True
        logger.loglevel(logger.DEBUG)

    logger.debug('> Read configuration from cmdline:')
    logger.debug(configuration)
    return configuration


CONFIG = Config()

__ALL__ = ['CONFIG']
