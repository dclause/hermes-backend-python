"""Get cli arguments used when starting the project."""
import argparse
from pathlib import Path
from typing import Any

from hermes import __version__


def _get_cli_args() -> dict[str, Any]:
    """
    Build configuration object from commandline parameters.

    Returns
    -------
        A list of configurations
    """
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('-h', '--host', action='store', dest='host', default='127.0.0.1',
                        help='Host (default 127.0.0.1)')
    parser.add_argument('-p', '--port', type=int, action='store', dest='port', default=8080,
                        help='Port number (default 8080)')
    parser.add_argument('--ssl', action='store', dest='ssl', default='certfiles',
                        help='Certifiers directory. Must contain privatekey.pem and certificate.pem files.')
    parser.add_argument('--trusted-host', action='store', dest='trusted', nargs='*', default=[],
                        help='A list of trusted hosts')
    parser.add_argument('--dev', action='store_true', dest='dev', help='Server development mode')
    parser.add_argument('--open', action='store_true', dest='open', help='Open the GUI in browser on startup')
    parser.add_argument('--debug', action='store_true', dest='debug')
    parser.add_argument('--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')

    parser.add_argument('--version',
                        action='version',
                        default=argparse.SUPPRESS,
                        version=f'HERMES version {__version__}')

    _args = vars(parser.parse_args())

    # Always allow localhost as a trusted host, as well as the current chosen host.
    _args['trusted'].append('localhost')
    _args['trusted'].append(_args['host'])
    # Check if certfiles are here to decide for ssl.
    if not Path(_args['ssl'], 'privatekey.pem').exists() or not Path(_args['ssl'], 'certificate.pem').exists():
        _args['ssl'] = None

    return {
        'debug': _args['debug'],
        'server': {
            'host': _args['host'],
            'port': _args['port'],
            'open': _args['open'],
            'reload': _args['dev'],
            'trusted': _args['trusted'],
            'ssl': _args['ssl'],
        },
    }


args = _get_cli_args()
