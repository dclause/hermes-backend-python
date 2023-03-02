"""
API package.
This package contains all definition and API specific implementation.
"""
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_socketio import SocketManager

from hermes.core import logger
from hermes.core.config import settings
from hermes.devices import AbstractDevice

_SOCKET = None


async def mutation(board_id: int, command_id: int, value: Any):
    try:
        device: AbstractDevice = settings.get('boards')[board_id].actions[command_id]
        device.set_value(board_id, value)
        settings.get('boards')[board_id].actions[command_id].state = value
    except Exception as exception:
        logger.error(f'Mutation error: "{exception}".')
        raise exception
    await _SOCKET.emit('patch', (board_id, settings.get('boards')[board_id].serialize(recursive=True)))


def init(app: FastAPI) -> None:
    """ Defines and attaches the API routes associated with a fastAPI server. """
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
            {key: board.serialize(recursive=True) for key, board in settings.get('boards').items()},
            settings.get('groups'),
        ))

    @_SOCKET.on('action')
    async def _mutation(cid: str, board_id: int, command_id: int, value: Any, *args, **kwargs):
        logger.debug(f'Socket client {cid}: Mutation with parameter: {board_id} {command_id} {value}')
        try:
            await mutation(board_id, command_id, value)
        except Exception as exception:
            logger.error(f'Mutation error for client {cid}.')
