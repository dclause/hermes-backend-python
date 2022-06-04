""" Implements agnostic custom structure types to be reused through the application. """

from abc import ABCMeta
from queue import Queue


class ClearableQueue(Queue):
    """ A custom queue subclass that provides a :meth:`clear` method. """

    def clear(self):
        """ Clears all items from the queue. """

        with self.mutex:
            unfinished = self.unfinished_tasks - len(self.queue)
            if unfinished <= 0:
                if unfinished < 0:
                    raise ValueError('task_done() called too many times')
                self.all_tasks_done.notify_all()
            self.unfinished_tasks = unfinished
            self.queue.clear()
            self.not_full.notify_all()


class ReadOnlyDict(dict):
    """ A dictionary where items cannot be updated. """

    def __setitem__(self, key, value):
        if key not in self:
            dict.__setitem__(self, key, value)
        else:
            raise KeyError("Key already exists")


class MetaSingleton(type):
    """ A type for Singleton classes. """

    def __init__(cls, *args):
        type.__init__(cls, *args)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = type.__call__(cls, *args, **kwargs)
        return cls.__instance


class MetaPluginType(type, metaclass=ABCMeta):
    """ A type for Plugin type classes. """

    def __init__(cls, name, bases, namespace):
        super(MetaPluginType, cls).__init__(name, bases, namespace)
        if not hasattr(cls, 'plugins'):
            cls.plugins = []
        else:
            cls.plugins.append(cls)
