"""Implements agnostic custom structure types to be reused through the application."""
from __future__ import annotations

import inspect
from abc import ABCMeta
from enum import Enum
from pathlib import Path
from queue import Queue
from typing import Any


class ClearableQueue(Queue[Any]):
    """A custom queue subclass that provides a :meth:`clear` method."""

    def clear(self) -> None:
        """Clear all items from the queue."""

        with self.mutex:
            unfinished = self.unfinished_tasks - len(self.queue)
            if unfinished <= 0:
                if unfinished < 0:
                    raise ValueError('task_done() called too many times')
                self.all_tasks_done.notify_all()
            self.unfinished_tasks = unfinished
            self.queue.clear()
            self.not_full.notify_all()


class ReadOnlyDict(dict[Any, Any]):
    """A dictionary subclass where items cannot be updated."""

    def __setitem__(self, key: Any, value: Any) -> None:
        if key not in self:
            dict.__setitem__(self, key, value)
        else:
            raise KeyError('Key already exists')


class MetaSingleton(type):
    """A meta type for Singleton classes."""

    def __init__(cls, *args: Any):
        type.__init__(cls, *args)
        cls.__instance = None

    def __call__(cls, *args: Any, **kwargs: Any) -> None:  # noqa: D102
        if not cls.__instance:
            cls.__instance = type.__call__(cls, *args, **kwargs)
        return cls.__instance


class MetaPluginType(type, metaclass=ABCMeta):
    """A type for Plugin type classes."""

    def __init__(cls, name: str, bases: Any, namespace: Any) -> None:
        super().__init__(name, bases, namespace)
        cls.folder = Path(inspect.getfile(cls.__class__)).parent.name
        if not hasattr(cls, 'plugins'):
            cls.plugins: list[type] = []
        else:
            cls.plugins.append(cls)


class StringEnum(str, Enum):
    """Enum where members are also (and must be) strings."""
