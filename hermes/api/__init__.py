"""
API package.
This package contains all definition and API specific implementation.
"""

from fastapi import FastAPI
from hermes import __version__


def init():
    """ Defines and returns the API routes associated with a fastAPI server. """
    app = FastAPI()

    @app.get("/")
    def healthcheck():
        return {'status': 'healthy', 'version': __version__}

    return app
