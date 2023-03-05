"""
Devices package.
This package contains all implemented devices provided by default in HERMES.

A device is a physical piece of electronic wired to a Board (ex: led, servo, etc...).
@see Board definition in boards package.

A device state is mutable via devices (@see Device definition in devices package).
The devices can be sent via the 'device' socketIO method.
@see :class:`Server` definition in server.py.
@see :class:`Device` definition in devices package.

Devices can be created from configs file leaving in the config/devices.yml file. Each device must validate the
schema provided within this package.
Devices are detected when the package is imported for the first time and globally available via the settings under
the `devices` key
"""
from __future__ import annotations

from abc import abstractmethod
from collections.abc import Callable
from typing import Any

from nicegui import ui

from hermes import gui
from hermes.core import logger
from hermes.core.config import settings
from hermes.core.dictionary import MessageCode
from hermes.core.logger import HermesError
from hermes.core.plugins import AbstractPlugin
from hermes.core.struct import MetaPluginType, MetaSingleton


class DeviceError(HermesError):
    """Base class for device related exceptions."""


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
        self.gui_actions = None
        self.default: Any = default
        self.state = default

    @property
    @abstractmethod
    def code(self) -> MessageCode:
        """Each device type must be a 8bit code from the MessageCode dictionary."""

    def render(self, mutator: Callable[[int, Any], None]) -> None:
        """
        Render a device using nicegui.io syntax.
        This method _can_ be overriden but is not meant to.
        """
        with gui.container().classes('device-icon'):
            icon = self.render_icon()
            if icon:
                gui.icon(icon).props('size="30px"')
        with gui.container().classes('device-name font-bold'):
            self.render_name()
        with gui.container().classes('device-info text-italic'):
            self.render_info()
        with gui.container().classes('device-action flex-grow') as actions:
            self.render_action(mutator)
        self.gui_actions = actions

    def render_icon(self) -> str:
        """Render the board icon (@see https://fonts.google.com/icons)."""
        return 'brightness_high'

    def render_name(self) -> None:
        """Render the board name."""
        ui.label().bind_text(self, 'name')

    def render_info(self) -> None:
        """
        Render extra info.
        Should typically be either a very short text (pin number for instance) or an 'info' icon with a tooltip.
        """

    def render_action(self, mutator: Callable[[int, Any], None]) -> None:
        """Render an actionable input to bind with the board action."""
        ui.label('No action here.').classes('text-italic')

    @abstractmethod
    def _encode_data(self) -> bytearray:
        """Encode the settings of the device as a byte array."""
        return bytearray()

    @abstractmethod
    def _encode_value(self, value: Any) -> bytearray:
        """Encode the given value as an array of bytes."""
        return bytearray([value])

    def as_playload(self) -> bytearray:
        """
        Return the representation of the device as a bytearray.
        This is used to:
         - describes the device to the physical board during the handshake process.
         - changes the settings of a device.
        """
        header = bytearray([self.code, self.id])
        data = self._encode_data()
        return bytearray([len(data) + 2]) + header + data

    def set_value(self, board_id: int, value: Any) -> None:
        """Send the command."""
        board: Any = settings.get(['boards', board_id])

        if not board.connected and not board.open():
            raise DeviceError(f'Board {board.id} ({board.name}) is not connected.')

        header = bytearray([MessageCode.MUTATION, self.id])
        data = self._encode_value(value)
        board.send(header + data)

    def __str__(self) -> str:
        return f'Device {self.name}'


class DeviceFactory(metaclass=MetaSingleton):
    """Device factory class: instantiates a Device of a given type."""

    def __init__(self) -> None:
        self.__devices: dict[MessageCode, AbstractDevice] = {}

        # Self registers all AbstractDevice defined plugins.
        for device in AbstractDevice.plugins:
            self.__devices[device().code] = device()

    def get_by_code(self, code: MessageCode) -> AbstractDevice:
        """
        Instantiate a AbstractDevice based on a given MessageCode.

        :param MessageCode code: The MessageCode of the Device to instantiate.

        :return AbstractDevice | None:

        :raise DeviceError: the device code does not exist.

        **See also:** :class:`MessageCode`
        """
        device = self.__devices.get(code)
        if device is None:
            logger.error(f'Device {code} do not exists.')
            raise DeviceError(f'Device with code `{code}` do not exists.')
        return device

    def get_by_name(self, name: str) -> AbstractDevice:
        """
        Instantiate a AbstractDevice based on a given name.

        :param str name: The name of the Device to instantiate.

        :return AbstractDevice or None:

        :raise DeviceError: the device name does not exist.

        **See Also:** :class:`MessageCode`
        """
        device = next((device for device in self.__devices.values() if device.name == name), None)
        if device is None:
            logger.error(f'Device {name} do not exists.')
            raise DeviceError(f'Device with name `{name}` do not exists.')
        return device


__ALL__ = ['AbstractDevice', 'DeviceFactory', 'DeviceError']
