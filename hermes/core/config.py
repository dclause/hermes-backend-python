"""
Configuration module.

Handles the configuration for the application. The configurations are stored in YAML files in a `config` package of a
given "space".
 - Default space is in `core` package and is given by the application itself
 - Plugins living in the `plugins` space can each have a `config` package overriding the configuration.
 - Finally the upmost specific configuration is the one given as parameters of the commandline when starting the
  application.
"""

from typing import Any, Dict

from mergedeep import merge

from hermes.core import storage, logger, cli
from hermes.core.struct import MetaSingleton


class Config(metaclass=MetaSingleton):
    """ Global config object """
    __config: Dict[str, Any] = {}

    def __init__(self):
        self.__config = cli.args

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


CONFIG = Config()

__ALL__ = ['CONFIG']
