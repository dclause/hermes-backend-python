"""
The server section is responsible for :
    - serves a default GUI (@see `gui` directory)
    - exposes the socket.io API to help remote UIs to send commands
        @see `https://github.com/dclause/hermes_vuejs` for an example.
"""
import contextlib
import threading
import time
from collections.abc import Generator
from pathlib import Path
from socket import socket
from typing import Any, cast

import uvicorn
from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from uvicorn import Config
from uvicorn.supervisors import ChangeReload

from hermes import __version__, gui
from hermes.core import api, logger, plugins, storage
from hermes.core.config import settings

server: Any


class _ChangeReloadServer(ChangeReload):  # type: ignore[valid-type, misc]
    """Overrides the default uvicorn server to run in a separated thread context."""

    def __init__(self, _server: uvicorn.Server, _config: Config, _sockets: list[socket]) -> None:
        super().__init__(_config, _server.run, _sockets)
        uvicorn.supervisors.basereload.HANDLED_SIGNALS = []  # type: ignore[assignment]
        self._server = _server
        self.started = False

    def run(self) -> None:
        self.started = True
        super().run()

    @contextlib.contextmanager
    def run_in_thread(self) -> Generator[None, None, None]:
        """To be called instead of uvicorn.run() to run the server in a dedicated thread."""
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self._server.should_exit = True
            self.should_exit.set()
            thread.join()


class _Server(uvicorn.Server):
    """Overrides the default uvicorn server to run in a separated thread context."""

    def install_signal_handlers(self) -> None:
        pass

    @contextlib.contextmanager
    def run_in_thread(self, sockets: list[socket] | None = None) -> Generator[None, None, None]:
        """To be called instead of uvicorn.run() to run the server in a dedicated thread."""
        thread = threading.Thread(target=self.run, args=(sockets,))
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()


def init() -> None:
    """Initialize the server."""
    global server  # noqa: PLW0603

    certfiles = cast(str, settings.get(['server', 'ssl']))
    config = Config(
        'hermes.core.server:reload_factory' if settings.get(['server', 'reload']) else 'hermes.core.server:factory',
        factory=True,
        host=settings.get(['server', 'host']),  # type: ignore[arg-type]
        port=settings.get(['server', 'port']),  # type: ignore[arg-type]
        log_level='warning',
        reload=settings.get(['server', 'reload']),  # type: ignore[arg-type]
        reload_includes=['*.py', '*.css'] if settings.get(['server', 'reload']) else None,
        ssl_keyfile=Path(certfiles, 'privatekey.pem').absolute().__str__() if certfiles else None,
        ssl_certfile=Path(certfiles, 'certificate.pem').absolute() if certfiles else None,
    )

    server = _Server(config=config)  # noqa: PLW0603
    if config.should_reload:
        sock = config.bind_socket()
        server = _ChangeReloadServer(_server=server, _config=config, _sockets=[sock])


def factory() -> FastAPI:
    """
    Initialize the server.
    @see --factory option in uvicorn: https://www.uvicorn.org/#application-factories.
    """
    app = FastAPI()

    app.add_middleware(HTTPSRedirectMiddleware)
    print(settings.get(['server', 'trusted']))
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.get(['server', 'trusted']))
    app.add_middleware(GZipMiddleware)

    @app.get('/version')
    def healthcheck() -> dict[str, str]:
        return {'status': 'healthy', 'version': __version__}

    api.init(app)
    gui.init(app)
    return app


def reload_factory() -> FastAPI:
    """
    Initialize the server - used for reloadable server option.
    Uses the standard factory but also reuses the hermes init() application bootstrap.
    @see factory().
    """
    logger.init()
    plugins.init()
    storage.init()
    settings.init()
    return factory()
