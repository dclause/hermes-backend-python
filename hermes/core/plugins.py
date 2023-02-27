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

import glob
import importlib
import itertools
import os
import pkgutil
from enum import Enum
from typing import Any, TypeVar

import hermes
from hermes.core import logger
from hermes.core.helpers import ROOT_DIR

TypeAbstractPlugin = TypeVar("TypeAbstractPlugin", bound="AbstractPlugin")


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

    def serialize(self, recursive=False) -> dict[str, Any]:
        """
        Convert the instance to a filter dict representation.
        Private attributes are excluded and Plugin referenced are converted to their IDs.

        Returns:
            dict[str, Any]: a dictionary where the keys are the class public attributes.
        """
        obj = vars(self).copy()
        for attr in vars(self):

            # Remove the private attributes to prevent them being serialized.
            if attr.startswith("_") and not attr.startswith("__"):
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
        """ Converts a representation node to a Python object. """

        # Builds a state object from the yaml data.
        state = constructor.construct_mapping(node, deep=True)

        # Filters the state object with values necessary for the plugin constructor.
        arguments = cls.__init__.__code__.co_varnames[1:cls.__init__.__code__.co_argcount]
        initial_state = {}
        for key in arguments:
            if key in state:
                initial_state[key] = state[key]

        # Instantiates the plugin and update it.
        plugin = cls(**initial_state)

        if 'default' in state:
            state['state'] = state['default']
        if hasattr(plugin, '__setstate__'):
            plugin.__setstate__(state)
        else:
            plugin.__dict__.update(state)

        return plugin

    @classmethod
    def to_yaml(cls, representer, data) -> Any:
        """ Converts a Python object to a representation node. """

        if isinstance(data, AbstractPlugin):
            data = data.serialize()
            if any(key in dict for key in ['value', 'type', 'container']):
                del data['value']

        tag = getattr(cls, 'yaml_tag', '!' + cls.__name__)
        return representer.represent_mapping(tag, data)


def init():
    """
    Loads all plugins.

    Explores the directory structure and search for all .py files within directories corresponding to plugin types
    to import it.
    The plugins could be in the core or the modules directories.
    @todo evaluation if there is a better way.
    """
    logger.info(" > Plugin discovery")


    # for name in pkgutil.walk_packages(hermes.__path__, hermes.__name__):
    #     print(f'Find {name}....')
    #     # importlib.import_module(f'hermes.{plugin_folder}.{modulename}')
    #
    # files = glob.glob(os.path.join(ROOT_DIR, '**', '*.py'), recursive=True)
    # plugin_folders = ['protocols', 'boards', 'devices', 'commands', 'pages']
    # for file in files:
    #     name = os.path.splitext(os.path.basename(file))[0]
    #     for plugin_folder in plugin_folders:
    #
    #     if plugin_folder in filepath and not filepath.endswith('__init__.py') and os.path.isfile(filepath):
    #     # add package prefix to name, if required
    #     module = __import__(name)
    #     for member in dir(module):
    #         pass
    # do something with the member named ``member``


    plugin_folders = ['protocols', 'boards', 'devices', 'commands']
    # Find all python files within the ROOT_DIR.
    modules = glob.glob(os.path.join(ROOT_DIR, '**', '*.py'), recursive=True)
    for filepath in modules:
        for plugin_folder in plugin_folders:
            # If the file is in one of plugin_folders folders, it surely is a plugin, hence load it.
            if plugin_folder in filepath and not filepath.endswith('__init__.py') and os.path.isfile(filepath):
                modulename = os.path.basename(filepath)[:-3]
                if 'hermes' + os.path.sep in filepath:
                    importlib.import_module(f'hermes.{plugin_folder}.{modulename}')
                if 'modules' + os.path.sep in filepath:
                    importlib.import_module(f'hermes.modules.{plugin_folder}.{modulename}')
