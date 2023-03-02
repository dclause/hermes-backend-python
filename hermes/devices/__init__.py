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

from nicegui import ui

from hermes import gui
from hermes.core import logger
from hermes.core.config import settings
from hermes.core.dictionary import MessageCode
from hermes.core.plugins import AbstractPlugin
from hermes.core.struct import MetaSingleton, MetaPluginType


class DeviceException(Exception):
    """ Base class for device related exceptions. """


class AbstractDevice(AbstractPlugin, metaclass=MetaPluginType):
    """
    Manages plugins of type devices.

    The properties of a device are :
    *id*            the device ID
    *name*          the device name
    *controller*    the device controller type (ie the class name of the device plugin type instance)
    *default*       the device default value
    ...
    any other properties brought by a board type plugin.
    (@see ServoDevice for example)
    """

    def __init__(self, default: Any = None):
        super().__init__()
        self.default: Any = default
        self.value = default

    @property
    @abstractmethod
    def code(self) -> MessageCode:
        """ Each device type must be a 8bit code from the MessageCode dictionary. """

    def render(self):
        """
        Renders a device using nicegui.io syntax.
        This method _can_ be overriden but is not meant to.
        """
        with gui.container().classes('device-icon'):
            icon = self.render_icon()
            if icon:
                ui.icon(icon).props('size="30px"')
        with gui.container().classes('device-name font-bold'):
            self.render_name()
        with gui.container().classes('device-info text-italic'):
            self.render_info()
        with gui.container().classes('device-action flex-grow'):
            self.render_action()

    @classmethod
    def render_icon(cls) -> str:
        """
        Renders the board icon (@see https://fonts.google.com/icons).
        """
        return 'brightness_high'

    def render_name(self):
        """
        Renders the board name.
        """
        ui.label().bind_text(self, 'name')

    @classmethod
    def render_info(cls):
        """
        Renders extra info.
        Should typically be either a very short text (pin number for instance) or an 'info' icon with an hover tooltip.
        """

    @classmethod
    def render_action(cls):
        """
        Renders an actionable input to bind with the board action.
        """
        ui.label('No action here.').classes('text-italic')

    @abstractmethod
    def _encode_data(self) -> bytearray:
        """ Encodes the settings of the device as a byte array. """
        return bytearray()

    @abstractmethod
    def _encode_value(self, value: any) -> bytearray:
        """ Encodes the given value as an array of bytes. """
        return bytearray([value])

    def as_playload(self) -> bytearray:
        """
        Returns the representation of the device as a bytearray.
        This is used to:
         - describes the device to the physical board during the handshake process.
         - changes the settings of a device
        """
        header = bytearray([self.code, self.id])
        data = self._encode_data()
        return bytearray([len(data) + 2]) + header + data

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
