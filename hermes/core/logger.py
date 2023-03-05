""" Logger specific functions. """

import inspect
import pathlib
import time

import logzero
from logzero import DEBUG, ERROR, INFO, WARNING, loglevel  # noqa: F401

from hermes.core import cli
from hermes.core.helpers import ROOT_DIR


def init(logpath: str = f'{ROOT_DIR}/logs/backend.log'):
    """
    Initialize logzero for the purpose of this project.

    :param str logpath: The path the logfile. Defaults to ./logs/backend.log
    """
    print(" > Init logger")

    # Create rotated logfile.
    pathlib.Path(logpath).parent.mkdir(parents=True, exist_ok=True)
    logzero.logfile(logpath, maxBytes=1000000, disableStderrLogger=True)
    logzero.logger.debug(' ===================================================== ')
    logzero.logger.debug('                        RESTART                        ')
    logzero.logger.debug(' ===================================================== ')

    # Custom formatter.
    formatter = logzero.LogFormatter(
        fmt='%(color)s[%(levelname)s - %(asctime)-15s - %(module)s:%(lineno)d]%(end_color)s %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S %p')
    logzero.formatter(formatter)
    # Log level.
    logzero.loglevel(logzero.DEBUG if cli.args['debug'] else logzero.INFO)


def debug(msg, *args, **kwargs):
    """ Forward DEBUG logs to logzero. """
    logzero.logger.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    """ Forward DEBUG logs to logzero. """
    print(msg.format(*args, **kwargs))
    logzero.logger.info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    """ Forward DEBUG logs to logzero. """
    print(f'\033[93m WARNING: {msg.format(*args, **kwargs)} \033[0m')
    logzero.logger.warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    """ Forward DEBUG logs to logzero. """
    print(f'\033[91m ERROR: {msg % args} \033[0m')
    logzero.logger.error(msg, *args, **kwargs)


def log(level, msg, *args, **kwargs):
    """ Forward logs to appropriate function. """
    match level:
        case logzero.DEBUG:
            return debug(msg, *args, **kwargs)
        case logzero.INFO:
            return info(msg, *args, **kwargs)
        case logzero.WARNING:
            return warning(msg, *args, **kwargs)
        case logzero.ERROR:
            return error(msg, *args, **kwargs)
    raise Exception(f'ErrorLevel not exists ({level})')


def logthis(*args):
    """
    Log decorator for a function: the call to this function will be logged and its performance measured.

    Examples
    --------
        Use a decorator on a function to log that function.
        ```
        @logthis
        def _decorated(self):
            pass
        ````

        By default, log is done with debug level, but it can be specified:
        ```
        @logthis(logger.WARNING)
        def _decorated(self):
            pass
        ````
    """

    def _log(function):
        def inner(*inner_args, **kwargs):
            """Inner method."""
            func_args_as_string = get_function_call_args(function, *inner_args, **kwargs)
            log(_loglevel, '> Start function %s', func_args_as_string)
            time_before = time.time()
            function(*inner_args, **kwargs)
            time_after = time.time()
            log(_loglevel, '> Function %s done (time: %s ms)',
                function.__name__,
                round((time_after - time_before) * 1000, 1),
                )

        def get_function_call_args(func, *func_args, **kwargs):
            """Return a string containing function name and list of all argument names/values."""
            func_args = inspect.signature(func).bind(*func_args, **kwargs)
            func_args.apply_defaults()
            func_args_str = ", ".join(f"{arg}={val}" for arg, val in func_args.arguments.items())
            return f"{func.__name__}({func_args_str})"

        return inner

    # If no argument passed, first args of decorator in the decorated function.
    if len(args) == 1 and callable(args[0]):
        _loglevel = logzero.DEBUG
        return _log(args[0])

    # If argument passed, first args is the given argument.
    _loglevel = args[0]
    return _log
