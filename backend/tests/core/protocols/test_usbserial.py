#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for the usbserial module."""

import unittest
from unittest.mock import MagicMock

import serial
from serial import SerialException

from hermes.core.commands import CommandCode
from hermes.core.protocols import ProtocolException
from hermes.core.protocols.usbserial import SerialProtocol


class SerialProtocolTest(unittest.TestCase):
    """Implements tests for the SerialProtocol class."""

    def setUp(self):
        """ Initialize test by mocking Serial class. """
        serial.Serial.open = MagicMock(name='serial.Serial.open')
        serial.Serial.close = MagicMock(name='serial.Serial.close')
        serial.Serial.inWaiting = MagicMock(name='serial.Serial.inWaiting')
        serial.Serial.read = MagicMock(name='serial.Serial.read')
        serial.Serial.isOpen = MagicMock(name='serial.Serial.isOpen')
        serial.Serial.write = MagicMock(name='serial.Serial.write')
        self._serial_protocol = SerialProtocol('COM3')

    def test_open(self):
        """ Tests serial protocol open. """
        try:
            self._serial_protocol.open()
        except ProtocolException:
            self.fail()
        # pylint: disable-next=no-member
        serial.Serial.open.assert_called_once()  # noqa

    def test_open_fail(self):
        """ Tests serial protocol open fails. """
        serial.Serial.open = MagicMock(name='serial.Serial.open', side_effect=SerialException('Boom!'))
        self.assertRaises(ProtocolException, self._serial_protocol.open)

    def test_close(self):
        """ Tests serial protocol open. """
        try:
            self._serial_protocol.close()
        except ProtocolException:
            self.fail()
        # pylint: disable-next=no-member
        serial.Serial.close.assert_called_once()  # noqa

    def test_isopen(self):
        """ Tests serial protocol is_open. """
        # True
        serial.Serial.isOpen = MagicMock(name='serial.Serial.isOpen', return_value=True)
        self.assertTrue(self._serial_protocol.is_open())
        # pylint: disable-next=no-member
        serial.Serial.isOpen.assert_called_once()  # noqa
        # False
        serial.Serial.isOpen = MagicMock(name='serial.Serial.isOpen', return_value=False)
        self.assertFalse(self._serial_protocol.is_open())
        # pylint: disable-next=no-member
        serial.Serial.isOpen.assert_called_once()  # noqa

    def test_read_command(self):
        """ Tests serial protocol read_command. """
        serial.Serial.read = MagicMock(name='serial.Serial.read', return_value=b'#')
        self.assertEqual(CommandCode.DEBUG, self._serial_protocol.read_command())

    def test_send_command(self):
        """ Tests serial protocol send_command. """
        self._serial_protocol.send_command(CommandCode.DEBUG)
        # pylint: disable-next=no-member
        serial.Serial.write.assert_called_once_with(b'#')  # noqa

    def test_read_line(self):
        """ Tests serial protocol read_line. """
        serial.Serial.read = MagicMock(name='serial.Serial.read', side_effect=[b'T', b'E',  b'S', b'T', b'\x0D', b'\x0A', b'S'])
        self.assertEqual("TEST", self._serial_protocol.read_line())
