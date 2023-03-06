"""Logger specific functions."""

import inspect
import pathlib
import time
from typing import Any

import logzero

from hermes.core import cli
from hermes.core.helpers import ROOT_DIR


class HermesError(Exception):
    """Generic exception through the application."""

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message)
        if message:
            error(message)


def init(logpath: str = f'{ROOT_DIR}/logs/backend.log') -> None:
    """
    Initialize logzero for the purpose of this project.

    :param str logpath: The path the logfile. Defaults to ./logs/backend.log
    """
    print(' > Init logger')

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


def debug(msg: Any, *args: Any, **kwargs: Any) -> None:
    """Forward DEBUG logs to logzero."""
    logzero.logger.debug(msg, *args, **kwargs)


def info(msg: Any, *args: Any, **kwargs: Any) -> None:
    """Forward INFO logs to logzero."""
    print(msg.format(*args, **kwargs))
    logzero.logger.info(msg, *args, **kwargs)


def warning(msg: Any, *args: Any, **kwargs: Any) -> None:
    """Forward WARNING logs to logzero."""
    print(f'\033[93m WARNING: {msg.format(*args, **kwargs)} \033[0m')
    logzero.logger.warning(msg, *args, **kwargs)


def error(msg: str, *args: Any, **kwargs: Any) -> None:
    """Forward ERROR logs to logzero."""
    print(f'\033[91m ERROR: {msg % args} \033[0m')
    logzero.logger.error(msg, *args, **kwargs)


def exception(msg: Any, *args: Any, **kwargs: Any) -> None:
    """Forward ERROR logs to logzero."""
    print(f'\033[91m EXCEPTION: {msg % args} \033[0m')
    logzero.logger.error(msg, *args, **kwargs)


def log(level: int, msg: Any, *args: Any, **kwargs: Any) -> None:
    """Forward logs to appropriate function."""
    match level:
        case logzero.DEBUG:
            return debug(msg, *args, **kwargs)
        case logzero.INFO:
            return info(msg, *args, **kwargs)
        case logzero.WARNING:
            return warning(msg, *args, **kwargs)
        case logzero.ERROR:
            return error(msg, *args, **kwargs)
    raise HermesError(f'ErrorLevel not exists ({level})')


# @todo should we keep this ?
def logthis(*args: Any) -> Any:
    """
    Log decorator for a function: the call to this function will be logged and its performance measured.

    **Example**
        Use a decorator on a function to log that function.
            ```
            @logthis
            def _decorated(self):
                pass
            ```

        By default, log is done with debug level, but it can be specified:
            ```
            @logthis(logger.WARNING)
            def _decorated(self):
                pass
            ```
    """

    def _log(function: Any) -> Any:
        def inner(*inner_args: Any, **kwargs: Any) -> None:
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

        def get_function_call_args(func: Any, *func_args: Any, **kwargs: Any) -> str:
            """Return a string containing function name and list of all argument names/values."""
            func_args_bounds: inspect.BoundArguments = inspect.signature(func).bind(*func_args, **kwargs)
            func_args_bounds.apply_defaults()
            func_args_str = ', '.join(f'{arg}={val}' for arg, val in func_args_bounds.arguments.items())
            return f'{func.__name__}({func_args_str})'

        return inner

    # If no argument passed, first args of decorator in the decorated function.
    if len(args) == 1 and callable(args[0]):
        _loglevel = logzero.DEBUG
        return _log(args[0])

    # If argument passed, first args is the given argument.
    _loglevel = args[0]
    return _log
