"""
Devices package.
This package contains all implemented devices provided by default in HERMES.

A device is a physical piece of electronic wired to a Board (ex: led, servo, etc...).
@see Board definition in boards package.

A device state is mutable via devices (@see Device definition in devices package).
The devices can be sent via the 'device' socketIO method.
@see Server definition in server.py.
@see Device definition in devices package.

Devices can be created from configs file leaving in the config/devices.yml file. Each device must validate the
schema provided within this package.
Devices are detected when the package is imported for the first time and globally available via the settings under
the `devices` key
"""
from abc import abstractmethod
from typing import Any

from hermes.core import logger
from hermes.core.config import settings
from hermes.core.dictionary import MessageCode
from hermes.core.plugins import AbstractPlugin
from hermes.core.struct import MetaSingleton, MetaPluginType


class DeviceException(Exception):
    """ Base class for device related exceptions. """


class AbstractDevice(AbstractPlugin, metaclass=MetaPluginType):
    """ Manages plugins of type devices. """

    def __init__(self):
        super().__init__()
        self.default: Any = None

    @property
    @abstractmethod
    def code(self) -> MessageCode:
        """ Each device type must be a 8bit code from the MessageCode dictionary. """

    @abstractmethod
    def _encode_settings(self) -> bytearray:
        """ Encodes the settings of the device as a byte array. """
        return bytearray()

    @abstractmethod
    def _encode_value(self, value: any) -> bytearray:
        """ Encodes the given value as an array of bytes. """
        return bytearray([value])

    def to_settings_payload(self) -> bytearray:
        """
        Returns the representation of the device as a bytearray.
        This is used to:
         - describes the device to the physical board during the handshake process.
         - changes the settings of a device
        """
        header = bytearray([self.code, self.id])
        settings = self._encode_settings()
        return bytearray([len(settings) + 2]) + header + settings

    def set_value(self, board_id, value: Any):
        """ Sends the command. """
        board = settings.get('boards')[board_id]

        if not board.connected:
            if not board.open():
                raise DeviceException(f'Board {board.id} ({board.name}) is not connected.')

        header = bytearray([MessageCode.MUTATION, self.id])
        data = self._encode_value(value)
        board.send(header + data)

    def __str__(self):
        return f'Device {self.name}'


class DeviceFactory(metaclass=MetaSingleton):
    """ Device factory class: instantiates a Device of a given type """

    def __init__(self):
        self.__devices: dict[MessageCode, AbstractDevice] = {}

        # Self registers all AbstractDevice defined plugins.
        for device in AbstractDevice.plugins:
            self.__devices[device().code] = device()

    def get_by_code(self, code: MessageCode) -> AbstractDevice | None:
        """ Instantiates a AbstractDevice based on a given MessageCode

        Args:
            code (MessageCode): The MessageCode of the Device to instantiate.
        Returns:
            AbstractDevice | None
        Raises:
            DeviceException: the device code does not exist.

        See Also:
            :class:`MessageCode`
        """
        device = self.__devices.get(code)
        if device is None:
            logger.error(f'Device {code} do not exists.')
            raise DeviceException(f'Device with code `{code}` do not exists.')
        return device

    def get_by_name(self, name: str) -> AbstractDevice | None:
        """ Instantiates a AbstractDevice based on a given name

        Args
            name (str): The name of the Device to instantiate.
        Returns
            AbstractDevice or None
        Raises:
            DeviceException: the device name does not exist.

        See Also:
            :class:`MessageCode`
        """
        device = next((device for device in self.__devices.values() if getattr(device, 'name') == name), None)
        if device is None:
            logger.error(f'Device {name} do not exists.')
            raise DeviceException(f'Device with name `{name}` do not exists.')
        return device


__ALL__ = ["AbstractDevice", "DeviceFactory"]
