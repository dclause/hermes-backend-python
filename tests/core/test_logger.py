#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Tests for the `core.logger` module. """

import os
import unittest

from hermes.core import logger
from hermes.core.logger import logthis

# Init logs to custom file.
_LOGPATH = './logs/testing.log'
logger.init(_LOGPATH)


class LoggerTest(unittest.TestCase):
    """ Tests for the logger file functions. """

    @logthis
    def _decorated_debug(self):
        pass

    @logthis(logger.INFO)
    def _decorated_info(self):
        pass

    @logthis(logger.WARNING)
    def _decorated_warning(self, dummy="foo"):
        logger.error(dummy)

    @classmethod
    def _get_last_log(cls):
        """
        Helper: get the last log in the logfile.

        Returns:
            str: The last line of the logfile.
        """
        with open(_LOGPATH, 'rb') as file:
            try:
                file.seek(-2, os.SEEK_END)
                while file.read(1) != b'\n':
                    file.seek(-2, os.SEEK_CUR)
            except OSError:
                file.seek(0)
            return file.readline().decode()

    def test_init(self):
        """ Log file should be created at given location when logger is initialized. """

        # Before test
        _custom_logpath = './logs/tmp.log'
        if os.path.exists(_custom_logpath):
            os.remove(_custom_logpath)
        self.assertFalse(os.path.exists(_custom_logpath))

        # Test
        logger.init(_custom_logpath)
        self.assertTrue(os.path.exists(_custom_logpath))

        # After test: back to _LOGPATH
        logger.init(_LOGPATH)
        if os.path.exists(_custom_logpath):
            os.remove(_custom_logpath)
        self.assertFalse(os.path.exists(_custom_logpath))

    def test_logger(self):
        """ Logger should log in file. """

        # Test error levels.
        for level, name in {
            logger.DEBUG: 'DEBUG',
            logger.INFO: 'INFO',
            logger.WARNING: 'WARNING',
            logger.ERROR: 'ERROR',
        }.items():
            logger.log(level, 'Log test %s (%s)', name, level)
            last_line = self._get_last_log()
            self.assertIn(f'[{name}', last_line)
            self.assertIn(f'Log test {name} ({level})', last_line)

        # Undefined level exception.
        self.assertRaises(Exception, logger.log, 'foo', 'bar')

    def test_decorator_logger(self):
        """ Decorator `@log` on a method/function should imply logging that method. """
        # Decorator by default: DEBUG
        self._decorated_debug()
        last_line = self._get_last_log()
        self.assertIn('DEBUG', last_line)
        self.assertIn('_decorated_debug', last_line)
        # Decorator with parameter: INFO
        self._decorated_info()
        last_line = self._get_last_log()
        self.assertIn('INFO', last_line)
        self.assertIn('_decorated_info', last_line)
        # Decorator on method with arguments, with parameter: WARNING
        self._decorated_warning()
        last_line = self._get_last_log()
        self.assertIn('WARNING', last_line)
        self.assertIn('_decorated_warning', last_line)
