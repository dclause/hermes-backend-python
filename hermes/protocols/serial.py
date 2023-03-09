"""
Serial communication handling.

Used by boards connected to the server via a USB serial cable.
"""

import glob
import sys

from serial import Serial, SerialException

from hermes.core import logger
from hermes.protocols import AbstractProtocol, ProtocolError


class SerialProtocol(AbstractProtocol):
    """Implements an :class:AbstractProtocol class using the serial port."""

    def __init__(self, port: str, baudrate: int = 115200, timeout: int = 0) -> None:
        super().__init__()
        self.port: str = port
        self.baudrate: int = baudrate
        self._timeout: int = timeout
        self._serial: Serial = Serial()

    def open(self) -> None:  # noqa: D102
        try:
            self._serial = Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self._timeout,
                writeTimeout=self._timeout,
            )
            self._serial.flush()
        except SerialException as error:
            logger.exception(f'Available ports are {self.get_serial_ports()}')
            raise ProtocolError(self, f'Port {self.port} could not be opened: {error}') from error

    def close(self) -> None:  # noqa: D102
        self._serial.close()

    def is_open(self) -> bool:  # noqa: D102
        return bool(self._serial.isOpen())

    def read_byte(self) -> int:  # noqa: D102
        bytes_array = None
        while not bytes_array:
            bytes_array = bytearray(self._serial.read(1))
        logger.debug(f'Serial protocol: Received command code {str(bytes_array[0])}')
        return bytes_array[0]

    def send(self, data: bytearray) -> None:  # noqa: D102
        logger.debug(f'Serial protocol: Send command {data} - {list(data)}')
        try:
            self._serial.write(data)
        except SerialException:
            ProtocolError(self, f'Error sending command {data} - {list(data)}')

    def read_line(self) -> str:  # noqa: D102
        response = ''
        while True:
            bytes_array = bytearray(self._serial.read(1))
            if bytes_array:
                response += chr(bytes_array[0])
            if '\r\n' in response:
                break
        return response.rstrip()

    @staticmethod
    def get_serial_ports() -> list[str]:
        """
        List serial ports.

        :return list[str]: A list of available serial ports.
        :raise EnvironmentError: The code is running on an unknown platform.
        """
        if sys.platform.startswith('win'):
            ports = [f'COM{(i + 1)}' for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # Exclude your current terminal "/dev/tty".
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise OSError('Unsupported platform')

        results = []
        for port in ports:
            try:
                connexion = Serial(port)
                connexion.close()
                results.append(port)
            except (OSError, SerialException):
                pass
        return results
