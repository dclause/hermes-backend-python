""" Implements global helper functions to be reused through the application. """
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CORE_DIR = os.path.join(ROOT_DIR, 'core')
CONFIG_DIR = os.path.join(ROOT_DIR, 'config')
PROFILE_DIR = os.path.join(ROOT_DIR, 'profiles')
PLUGIN_DIR = os.path.join(ROOT_DIR, 'plugins')


def combine_classes(*args):
    """ Combines classes. """
    name = "".join(a.__name__ for a in args)
    return type(name, args, {})
