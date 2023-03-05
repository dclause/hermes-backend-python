"""Implements global helper functions to be reused through the application."""
from pathlib import Path

import hermes
from hermes.core import logger

APP_DIR = Path(hermes.__file__).parent.absolute()
ROOT_DIR = Path(APP_DIR, '..').resolve().absolute()
MODULES_DIR = Path(APP_DIR, 'modules').resolve().absolute()
CONFIG_DIR = Path(APP_DIR, 'config').resolve().absolute()
PROFILE_DIR = Path(APP_DIR, 'profiles').resolve().absolute()


class HermesError(Exception):
    """Generic exception through the application."""

    def __init__(self, message: str = None):
        super().__init__(message)
        logger.error(message)
