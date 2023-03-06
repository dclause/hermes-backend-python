"""Implements global helper functions to be reused through the application."""

from pathlib import Path

import hermes

APP_DIR = Path(hermes.__file__).parent.absolute()
ROOT_DIR = Path(APP_DIR, '..').resolve().absolute()
MODULES_DIR = Path(APP_DIR, 'modules').resolve().absolute()
CONFIG_DIR = Path(APP_DIR, 'config').resolve().absolute()
PROFILE_DIR = Path(APP_DIR, 'profiles').resolve().absolute()
