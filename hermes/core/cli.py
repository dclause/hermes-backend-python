""" Get cli arguments used when starting the project. """
import argparse
from typing import MutableMapping, Any

from hermes import __version__


def _get_cli_args() -> dict[str, Any]:
    """
    Build configuration object from commandline parameters.

    Returns:
        MutableMapping: A list of configurations
    """
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('-h', '--host', action='store', dest='host', default='127.0.0.1',
                        help='Host (default 127.0.0.1)')
    parser.add_argument('-p', '--port', action='store', dest='port', default=8080, help='Port number (default 8080)')
    parser.add_argument('--dev', action='store_true', dest='dev', help='Server development mode')
    parser.add_argument('--open', action='store_true', dest='open', help='Open the GUI in browser on startup')
    parser.add_argument('--debug', action='store_true', dest='debug')
    parser.add_argument('--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')

    parser.add_argument('--version',
                        action='version',
                        default=argparse.SUPPRESS,
                        version=f'HERMES version {__version__}')

    return vars(parser.parse_args())


args = _get_cli_args()
