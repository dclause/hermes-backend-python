#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for the command module."""

import unittest

from hermes.core.commands import CommandFactory
from hermes.core.commands.blink import CommandCode
from hermes.core.commands.debug import DebugCommand
from hermes.core.commands.servo import ServoCommand


class CommandFactoryTest(unittest.TestCase):
    """Implements tests for the CommandFactory class."""

    def test_singleton(self):
        """Test the CommandFactory to be a proper singleton."""
        self.assertEqual(CommandFactory(), CommandFactory())

    def test_get_by_code(self):
        """Test the CommandFactory get_by_code. Expects a AbstractCommand or None"""
        self.assertIsInstance(CommandFactory().get_by_code(CommandCode.DEBUG), DebugCommand)
        self.assertIs(CommandFactory().get_by_name('UNKNOWN'), None)

    def test_get_by_name(self):
        """Test the CommandFactory get_by_name. Expects a AbstractCommand or None"""
        self.assertIsInstance(CommandFactory().get_by_name('SERVO'), ServoCommand)
        self.assertIs(CommandFactory().get_by_name('UNKNOWN'), None)
