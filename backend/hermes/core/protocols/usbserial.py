"""
Serial communication handling.
Used by boards in serial mode (only supported mode as of today).

--
TLDR: To send a command, ClearableQueue it. That ClearableQueue is consumed by a dedicated thread of each board
(CommandSenderThread) which actually sends the command. The number of commands sent is limited until ACK are received to
prevent growing the serial buffer (SerialListenerThread).
--

This package introduces multithreading to handle communication over the serial port.

Commands that need to be sent over `serial` should be queues using a :class:CommandQueue.

- The class :class:CommandThread defines a separated thread which role is to consume that ClearableQueue and actually
send the commands. It can only send a given amount of commands, hence the CommandQueue acting as a waiting
ClearableQueue.
The number of commands sent is tracked via a semaphore and only frees the way when the corresponding ACK is received.

- The class :class:ListenerThread defines a separated which role is to receive data from the serial communication and
execute the corresponding command. It is also frees the semaphore when receiving ACK to let the :class:CommandThread
continue its work on sending queued commands.
"""

import glob
import sys

from serial import Serial, SerialException

from hermes.core import logger
from hermes.core.protocols import AbstractProtocol, ProtocolException


class SerialProtocol(AbstractProtocol):
    """ Implements an :class:AbstractProtocol class using the serial port. """

    def __init__(self, serial_port, baudrate=115200, timeout=0, write_timeout=0):
        self._serial_port: bool = serial_port
        self._baudrate: int = baudrate
        self._timeout: int = timeout
        self._write_timeout: int = write_timeout
        self._serial: Serial = Serial()

    def open(self) -> None:
        try:
            self._serial = Serial(
                port=self._serial_port,
                baudrate=self._baudrate,
                timeout=self._timeout,
                writeTimeout=self._write_timeout
            )
            self._serial.flush()
        except SerialException as error:
            logger.error(f'Serial connexion: Port {self._serial_port} could not be opened.')
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
        logger.debug(f'Serial protocol: Send command {data}')
        self._serial.write(data)

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
        for port in ports:
            try:
                connexion = Serial(port)
                connexion.close()
                results.append(port)
            except (OSError, SerialException):
                pass
        return results
