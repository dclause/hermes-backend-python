"""
Handles plugins discovery.

Plugins are classes of any plugin-like abstract types:
    - protocol (@see hermes.core.protocols): defines communication protocols between boards.
    - board (@see hermes.core.boards): defines supported board types (raspberry, arduino, etc...)
    - device (@see hermes.core.devices): defines supported device types (led, servo, etc...)
    - command (@see hermes.core.commands): defines supported command types (blink, servo, debug, etc...)

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

from hermes.core.helpers import ROOT_DIR


class AbstractPlugin:
    """
    A serializable plugin base class.

    Such a class is :
        - a plugin: it can be auto-discovered as it is loaded (@see plugins.py)
        - serializable: the implementation of a plugin of this type can be loader / saved in YAML file (@see plugins.py)
        - auto-incremented ID: it has a unique ID auto-incremented (if not provided) when instantiated.
        - named: it has a human-readable name
    """

    _id_iter = itertools.count(1)

    def __init__(self, name):
        self.id = next(self._id_iter)
        self.name: str = name

    def __str__(self):
        return f'{self.__class__.__name__} {self.name}({self.id})'

    @classmethod
    def from_yaml(cls, loader, node):
        """ Converts a representation node to a Python object. """
        return loader.construct_yaml_object(node, cls)

    @classmethod
    def to_yaml(cls, dumper, data):
        """ Converts a Python object to a representation node. """

        state = data.__dict__.copy()
        for attr in data.__dict__:

            # Remove the private attributes to prevent them being serialized.
            if attr.startswith("_") and not attr.startswith("__"):
                del state[attr]
                continue

            # Convert plugins reference to IDs (will be undone in CONFIG loading).
            if isinstance(state[attr], AbstractPlugin):
                state[attr] = state[attr].id

        tag = getattr(cls, 'yaml_tag', '!' + cls.__name__)
        return dumper.represent_mapping(tag, state)

    def __repr__(self):
        return f"{self.__class__.__name__,}(name={self.name})"


def init():
    """
    Loads all plugins.

    Explores the directory structure and search for all .py files within directories corresponding to plugin types.
    The plugins should be in the core or the modules directories.
    """
    print(" > Plugin discovery")

    plugin_types = ['protocol', 'board', 'device', 'command']
    modules = glob.glob(os.path.join(ROOT_DIR, '**', '*.py'), recursive=True)
    for filepath in modules:
        for plugin_type in plugin_types:
            plugin_type = plugin_type + 's'
            if plugin_type in filepath and not filepath.endswith('__init__.py') and os.path.isfile(filepath):
                modulename = os.path.basename(filepath)[:-3]
                importlib.import_module(f'hermes.core.{plugin_type}.{modulename}')
