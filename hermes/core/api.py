"""
API package.
This package contains all definition and API specific implementation.
"""
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_socketio import SocketManager
from nicegui import ui

from hermes.core import logger
from hermes.core.config import settings
from hermes.core.helpers import HermesException
from hermes.devices import AbstractDevice

_SOCKET: SocketManager


async def action(cid: str, board_id: int, device_id: int, value: Any) -> None:
    """
    Perform an action on the given board.

    :param str cid:         the client id requesting the action.
    :param int board_id:    the board id to perform the action on.
    :param int device_id:   the device id to perform the action on.
    :param any value:       the value to change to.
    """
    logger.debug(f'Client {cid}: Mutation with parameter: {board_id} {device_id} {value}')
    try:
        device: AbstractDevice = settings.get(['boards', board_id, 'actions', device_id])
        device.set_value(board_id, value)
        # @todo implement and use set()
        settings.get('boards')[board_id].actions[device_id].state = value
        ui.update(settings.get(['boards', board_id, 'actions', device_id]).gui_actions)
        await _SOCKET.emit('action', (board_id, device_id, value), skip_sid=cid)
    except HermesException as exception:
        logger.error(f'API ERROR: Client {cid}: Mutation error: "{exception}".')


def init(app: FastAPI) -> None:
    """ Defines and attaches the API routes associated with a fastAPI server. """

    # pylint: disable-next=global-statement
    global _SOCKET

    _SOCKET = SocketManager(app=app, mount_location='/api', cors_allowed_origins=[])
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=["*"],
        allow_credentials=True,
        allow_headers=["*"],
    )

    @_SOCKET.on('connect')
    async def connect(cid: str, *args, **kwargs):
        logger.debug(f'Socket client {cid}: new client connected.')
        await handshake(cid)

    @_SOCKET.on('disconnect')
    def disconnect(cid: str, *args, **kwargs):
        logger.debug(f'Socket client {cid}: client disconnected.')

    @_SOCKET.on('ping')
    def ping(cid: str):
        """
        Answer to a ping by a pong.
        This can be used by the clients to check the latency of a ping/pong message exchange with this server.
        """
        _SOCKET.emit('pong', to=cid)

    @_SOCKET.on('handshake')
    async def handshake(cid: str, *args, **kwargs):
        """
        Pushes all current config to the client.
        """
        logger.debug(f'Socket client {cid}: ask for handshake.')
        await _SOCKET.emit('handshake', (
            settings.get('global'),
            settings.get('profile'),
            {key: board.serialize() for key, board in settings.get('boards').items()},
            settings.get('groups'),
        ))

    @_SOCKET.on('action')
    async def _action(cid: str, board_id: int, command_id: int, value: Any, *args, **kwargs):
        await action(cid, board_id, command_id, value)


__ALL__ = ['init', 'action']
