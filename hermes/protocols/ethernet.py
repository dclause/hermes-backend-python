"""
Ethernet communication handling.

Used by boards connected via an RJ45, usually through an appropriate ethernet shield.
"""
import contextlib
import socket

from hermes.core import logger
from hermes.core.logger import HermesError
from hermes.protocols import AbstractProtocol


class EthernetProtocol(AbstractProtocol):
    """Implements an :class:AbstractProtocol class using the ethernet port."""

    def __init__(self, ip: str, port: int = 5000, timeout: int = 1) -> None:
        super().__init__()
        self.ip: str = ip
        self.port: int = port
        self._client = (self.ip, self.port)
        self._timeout: int = timeout
        self._socket: socket.SocketType = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.settimeout(self._timeout)
        self._is_open = False

    def open(self) -> None:  # noqa: D102
        try:
            self._socket.connect(self._client)
        except socket.error as error:  # noqa: UP024
            raise HermesError(f'Ethernet protocol: Address {self._client} could not be reached: {error}') from error
        self._is_open = True

    def close(self) -> None:  # noqa: D102
        self._socket.close()
        self._is_open = False

    def is_open(self) -> bool:  # noqa: D102
        return self._is_open

    def read_byte(self) -> int:  # noqa: D102
        bytes_array = None
        while not bytes_array:
            with contextlib.suppress(socket.error):
                bytes_array = bytearray(self._socket.recv(1))
        logger.debug(f'Serial protocol: Received command code {str(bytes_array[0])}')
        return bytes_array[0]

    def send(self, data: bytearray) -> None:  # noqa: D102
        logger.debug(f'Ethernet protocol: Send command {data} - {list(data)}')
        try:
            self._socket.send(data)
        except socket.error as error:  # noqa: UP024
            HermesError(f'Ethernet protocol: Error sending command {data} - {list(data)} : {error}')

    def read_line(self) -> str:  # noqa: D102
        response = ''
        while True:
            bytes_array = bytearray(self._socket.recv(1))
            if bytes_array:
                response += chr(bytes_array[0])
            if '\r\n' in response:
                break
        return response.rstrip()
