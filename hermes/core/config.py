"""
Configuration module.

Handles the configuration for the application. The configurations are stored in YAML files in a `config` package of a
given "space".
 - Default space is in `core` package and is given by the application itself
 - Plugins living in the `plugins` space can each have a `config` package overriding the configuration.
 - Finally the upmost specific configuration is the one given as parameters of the commandline when starting the
  application.
"""

from typing import Any, Dict, List

from mergedeep import merge

from hermes.core import storage, logger, cli
from hermes.core.struct import MetaSingleton


class ConfigException(Exception):
    """ Base class for plugin related exceptions. """


class _Settings(metaclass=MetaSingleton):
    """ Global config object """
    data: Dict[str, Any] = {}

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

        _Settings.data = storage.load()
        merge(_Settings.data, cli.args)

        logger.debug('> Total build configuration:')
        logger.debug(_Settings.data)

    @staticmethod
    def get(path: str | List[str] = None) -> dict[str, Any]:
        """ Gets a configuration value following the given path. """
        if path is None:
            return _Settings.data
        if isinstance(path, str):
            path = [path]

        current = _Settings.data
        for key in path:
            if key not in current:
                raise ConfigException(f"No settings for key {key}.")
            current = current[key]
        return current

    @staticmethod
    def set(path: str | List[str], value: Any) -> None:
        """ Sets a configuration value following the given path. """
        if isinstance(path, str):
            path = [path]
        if len(path) == 0:
            raise ConfigException('Path cannot be empty.')

        current = _Settings.data
        for key in path[:-1]:
            if key not in current:
                raise ConfigException(f'No settings for key {key}.')
            current = current[key]

        key = path[-1]
        current[key] = value


settings = _Settings()

__ALL__ = ['settings']
