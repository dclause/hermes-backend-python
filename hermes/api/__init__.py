"""
API package.
This package contains all definition and API specific implementation.
"""
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_socketio import SocketManager

from hermes.core import logger
from hermes.core.config import CONFIG
from hermes.devices import AbstractDevice


def init(app: FastAPI) -> None:
    """ Defines and attaches the API routes associated with a fastAPI server. """
    socket = SocketManager(app=app, mount_location='/api', cors_allowed_origins=[])
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=["*"],
        allow_credentials=True,
        allow_headers=["*"],
    )

    @socket.on('connect')
    async def connect(cid: str, *args, **kwargs):
        logger.info(f'Socket client {cid}: new client connected.')
        await handshake(cid)

    @socket.on('disconnect')
    def disconnect(cid: str, *args, **kwargs):
        logger.info(f'Socket client {cid}: client disconnected.')

    @socket.on('ping')
    def ping(cid: str):
        """
        Answer to a ping by a pong.
        This can be used by the clients to check the latency of a ping/pong message exchange with this server.
        """
        socket.emit('pong', to=cid)

    @socket.on('handshake')
    async def handshake(cid: str, *args, **kwargs):
        """
        Pushes all current config to the client.
        """
        logger.debug(f'Socket client {cid}: ask for handshake.')
        await socket.emit('handshake', (
            CONFIG.get('global'),
            CONFIG.get('profile'),
            {key: board.serialize(recursive=True) for key, board in CONFIG.get('boards').items()},
            CONFIG.get('groups'),
        ))

    @socket.on('action')
    async def mutation(cid: str, board_id: int, command_id: int, value: Any, *args, **kwargs):
        logger.debug(f'Socket client {cid}: Mutation with parameter: {board_id} {command_id} {value}')
        try:
            device: AbstractDevice = CONFIG.get('boards')[board_id].actions[command_id]
            device.set_value(board_id, value)
            CONFIG.get('boards')[board_id].actions[command_id].state = value
        except Exception as exception:
            logger.error(f'Socket client {cid}: Mutation error: "{exception}".')
        await socket.emit('patch', (board_id, CONFIG.get('boards')[board_id].serialize(recursive=True)))
