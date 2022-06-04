""" Logger specific functions. """

import inspect
import pathlib
import time

import logzero
# pylint: disable-next=unused-import
from logzero import DEBUG, INFO, WARNING, ERROR  # noqa: F401


def init(logpath: str = './logs/backend.log'):
    """
    Initializes logzero for the purpose of this project.

    Args:
        logpath (str): The path the logfile. Defaults to ./logs/backend.log
    """
    print(" > Init logger")
    logzero.loglevel(logzero.INFO)

    # Create rotated logfile.
    pathlib.Path(logpath).parent.mkdir(parents=True, exist_ok=True)
    logzero.logfile(logpath, maxBytes=1000000, loglevel=logzero.DEBUG, disableStderrLogger=True)

    # Custom formatter.
    formatter = logzero.LogFormatter(
        fmt='%(color)s[%(levelname)s - %(asctime)-15s - %(module)s:%(lineno)d]%(end_color)s %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S %p')
    logzero.formatter(formatter)


def debug(msg, *args, **kwargs):
    """ Forwards DEBUG logs to logzero. """
    logzero.logger.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    """ Forwards DEBUG logs to logzero. """
    logzero.logger.info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    """ Forwards DEBUG logs to logzero. """
    print(f'*** WARNING: {msg.format(*args, **kwargs)} ***')
    logzero.logger.warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    """ Forwards DEBUG logs to logzero. """
    print(f'*** ERROR: {msg % args} ***')
    logzero.logger.error(msg, *args, **kwargs)


def log(level, msg, *args, **kwargs):
    """ Forwards logs to appropriate function. """
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
    Log decorator for a function.

    Examples
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
            log(loglevel, '> Start function %s', func_args_as_string)
            time_before = time.time()
            function(*inner_args, **kwargs)
            time_after = time.time()
            log(loglevel, '> Function %s done (time: %s ms)',
                function.__name__,
                round((time_after - time_before) * 1000, 1)
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
        loglevel = logzero.DEBUG
        return _log(args[0])

    # If argument passed, first args is the given argument.
    loglevel = args[0]
    return _log
