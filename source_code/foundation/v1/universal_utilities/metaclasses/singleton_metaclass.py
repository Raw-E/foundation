from abc import ABCMeta
from threading import Lock
from typing import Final


class SingletonMetaclass(type):
    _lock: Final[Lock] = Lock()

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class ABCSingletonMetaclass(ABCMeta, SingletonMetaclass):
    pass
