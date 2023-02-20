"""
Serial communication handling.
Used by boards with SERIAL protocol type (only supported mode as of today).
"""

import glob
import sys

from serial import Serial, SerialException

from hermes.core import logger
from hermes.protocols import AbstractProtocol, ProtocolException


class SerialProtocol(AbstractProtocol):
    """ Implements an :class:AbstractProtocol class using the serial port. """

    def __init__(self, port, baudrate=115200, timeout=0):
        super().__init__()
        self._serial_port: bool = port
        self._baudrate: int = baudrate
        self._timeout: int = timeout
        self._serial: Serial = Serial()

    def open(self) -> None:
        try:
            self._serial = Serial(
                port=self._serial_port,
                baudrate=self._baudrate,
                timeout=self._timeout,
                writeTimeout=self._timeout
            )
            self._serial.flush()
        except SerialException as error:
            logger.error(f'Serial connexion: Port {self._serial_port} could not be opened: {error}')
            logger.info(f'Available ports are {self.get_serial_ports()}')
            raise ProtocolException(
                f'Port {self._serial_port} could not be opened'
            ) from error

    def close(self) -> None:
        self._serial.close()

    def is_open(self) -> bool:
        return self._serial.isOpen()

    def read_byte(self) -> int:
        bytes_array = None
        while not bytes_array:
            bytes_array = bytearray(self._serial.read(1))
        logger.debug(f'Serial protocol: Received command code {str(bytes_array[0])}')
        return bytes_array[0]

    def send(self, data: bytearray) -> None:
        logger.debug(f'Serial protocol: Send command {data} - {list(data)}')
        try:
            self._serial.write(data)
        except SerialException:
            logger.error(f'Serial protocol: Error sending command {data} - {list(data)}')

    def read_line(self) -> str:
        response = ""
        while True:
            bytes_array = bytearray(self._serial.read(1))
            if bytes_array:
                response += chr(bytes_array[0])
            if "\r\n" in response:
                break
        return response.rstrip()

    @staticmethod
    def get_serial_ports() -> list[str]:
        """
        Lists serial ports.

        Returns:
            list[str]: A list of available serial ports.

        Raises:
            EnvironmentError: The code is running on an unknown platform.
        """
        if sys.platform.startswith('win'):
            ports = [f'COM{(i + 1)}' for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # Exclude your current terminal "/dev/tty".
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        results = []
        print(ports)
        for port in ports:
            try:
                connexion = Serial(port)
                connexion.close()
                results.append(port)
            except (OSError, SerialException) as error:
                print(error)
                pass
        return results
