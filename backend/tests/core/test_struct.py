#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Tests for the `core.struct` module. """

import unittest

from hermes.core.struct import MetaPluginType
from hermes.core.struct import MetaSingleton


class StructTest(unittest.TestCase):
    """ Tests for the logger file functions. """

    def test_singleton(self):
        """ Tests the uniqueness of a Singleton. """

        class SingletonTest(metaclass=MetaSingleton):
            """ Testing purpose singleton class. """

        self.assertEqual(SingletonTest(), SingletonTest())

    def test_plugin(self):
        """ Tests the plugin metaclass autodiscovery. """

        class PluginTestType(metaclass=MetaPluginType):
            """ Testing purpose plugin type. """

        # pylint: disable-next=unused-variable
        class PluginTestA(PluginTestType):
            """ A testing purpose plugin of type PluginTestType. """

        # pylint: disable-next=unused-variable
        class PluginTestB(PluginTestType):
            """ A testing purpose plugin of type PluginTestType. """

        self.assertEqual(len(PluginTestType.plugins), 2)
