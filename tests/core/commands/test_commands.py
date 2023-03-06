#!/usr/bin/env python3

"""Tests for the command module."""

import unittest

from hermes.commands import CommandFactory
from hermes.commands.debug import DebugCommand
from hermes.commands.servo import ServoCommand
from hermes.core.dictionary import MessageCode


class CommandFactoryTest(unittest.TestCase):
    """Implements tests for the CommandFactory class."""

    def test_singleton(self):
        """Test the CommandFactory to be a proper singleton."""
        self.assertEqual(CommandFactory(), CommandFactory())

    def test_get_by_code(self):
        """Test the CommandFactory get_by_code. Expects a AbstractCommand or None."""
        self.assertIsInstance(CommandFactory().get_by_code(MessageCode.DEBUG), DebugCommand)
        self.assertIs(CommandFactory().get_by_name('UNKNOWN'), None)

    def test_get_by_name(self):
        """Test the CommandFactory get_by_name. Expects a AbstractCommand or None."""
        self.assertIsInstance(CommandFactory().get_by_name('SERVO'), ServoCommand)
        self.assertIs(CommandFactory().get_by_name('UNKNOWN'), None)
