"""
Handles plugins discovery.

Plugins are classes of any plugin-like abstract types:
    - protocol (@see hermes.protocols): defines communication protocols between boards.
    - board (@see hermes.boards): defines supported board types (raspberry, arduino, etc...)
    - device (@see hermes.devices): defines supported device types (led, servo, etc...)
    - command (@see hermes.commands): defines supported command types (blink, servo, debug, etc...)

The discovery of a plugin (foobar) of a given type (xxx) consists of loading the file containing its class definition
located at either of these locations:
- hermes.core.xxx.foobar.py
- hermes.module.xxx.foobar.py

Loading those plugins will - with the help of @see MetaPluginType - populate the plugin list via the corresponding
abstract plugin class (AbstractDevice, AbstractBoard, etc..). The list of all possible devices for instance can be found
via `AbstractDevice.plugins`.
"""

import importlib
import importlib.util
import itertools
from enum import Enum
from pathlib import Path
from typing import Any, Type, TypeVar

from hermes.core import logger
from hermes.core.helpers import ROOT_DIR, HermesException


class PluginException(HermesException):
    """ Base class for plugin related exceptions. """


TypeAbstractPlugin = TypeVar("TypeAbstractPlugin", bound="AbstractPlugin")

PLUGIN_TYPE_FOLDERS = ['protocols', 'boards', 'devices', 'commands']


class AbstractPlugin:
    """
    A serializable plugin base class.

    Such a class is :
        - a plugin: it can be auto-discovered as it is loaded (@see plugins.py)
        - serializable: the implementation of a plugin of this type can be loader / saved in YAML file (@see plugins.py)
        - auto-incremented ID: it has a unique ID auto-incremented (if not provided) when instantiated.
        - named: it has a human-readable name
    """

    # Custom IDs can be set using the YAML configuration file. But this lets IDs to be auto-generated for convenience
    # by increment from the last existing ID in the system.
    _id_iter = itertools.count(1)

    def __init__(self):
        self.id = next(self._id_iter)
        self.name: str = self.__class__.__name__
        self.controller: str = self.__class__.__name__

    def __str__(self):
        """ Stringify the plugin: Only used for debug purpose. """
        return f'{self.controller} {self.name}({self.id})'

    def __iter__(self, *args, **kwargs):  # real signature unknown
        """ Implement iter(self). """
        return [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a))]

    def __contains__(self, attr, *args, **kwargs):  # real signature unknown
        """ Check if attr is an attribute or method of the class. """
        return attr in dir(self)

    def __getitem__(self, y):  # real signature unknown; restored from __doc__
        """ Allow syntax equivalence x[y]. """
        return getattr(self, y)

    def serialize(self, recursive=True) -> dict[str, Any]:
        """
        Convert the instance to a filter dict representation.

        Private attributes are excluded and Plugin referenced are converted to their IDs.

        :return dict[str, Any]: a dictionary where the keys are the class public attributes.
        """
        obj = vars(self).copy()
        for attr in vars(self):

            # Remove the private attributes to prevent them being serialized.
            if attr.startswith("_") and not attr.startswith("__"):
                del obj[attr]
                continue

            # Remove any gui attributes.
            if attr.startswith("gui_"):
                del obj[attr]
                continue

            if recursive and isinstance(obj[attr], dict):
                listing = {element.id: element.serialize() for (key, element) in obj[attr].items()}
                obj[attr] = listing

            if recursive and isinstance(obj[attr], AbstractPlugin):
                obj[attr] = obj[attr].serialize()

            # Convert enum to their names.
            if isinstance(obj[attr], Enum):
                obj[attr] = obj[attr].name

        return obj

    @classmethod
    def from_yaml(cls, constructor, node) -> TypeAbstractPlugin:
        """ Convert a representation YAML node to a Python object. """

        # Extracts the data from the yaml data.
        mapping = constructor.construct_mapping(node, deep=True)

        # Analyzes the plugin constructor to determine the needed constructor parameters.
        arguments = cls.__init__.__code__.co_varnames[1:cls.__init__.__code__.co_argcount]

        # Extracts necessary constructor arguments from the mapping.
        init_args = {key: mapping[key] for key in arguments if key in mapping}

        # Instantiates the plugin.
        plugin = cls(**init_args)

        # Sets the plugin values to the required values such as extracted from the YAML files.
        plugin.__dict__.update(mapping)

        return plugin

    @classmethod
    def to_yaml(cls, representer, instance) -> Any:
        """ Convert a Python object to a representation node. """
        # Note: The yaml_tag used is by convention the classe name.
        tag = getattr(cls, 'yaml_tag', '!' + cls.__name__)
        return representer.represent_mapping(tag, instance.serialize())

    @staticmethod
    def types() -> list[Type[TypeAbstractPlugin]]:
        """ Return all plugin types within the application. """
        return AbstractPlugin.__subclasses__()


def init():
    """
    Load all plugins.

    Explores the directory structure and search for all .py files within directories corresponding to plugin types
    to import it. The plugins could be in the hermes or the modules directories.
    """
    logger.info(" > Plugin discovery")

    # @todo: let modules extend this list.
    namespaces = ['protocols', 'commands', 'devices', 'boards', 'gui.pages']
    for scope in ['hermes', 'modules']:
        for namespace in namespaces:
            loadable_plugins = Path(ROOT_DIR).glob('/'.join([scope, namespace.replace('.', '/'), '[!_]*.py']))
            for loadable_plugin in loadable_plugins:
                modulename = loadable_plugin.name[:-3]
                importlib.import_module(f'{scope}.{namespace}.{modulename}')
