
import functools
from typing import Callable, Any

import config
from . import logs


class __Dryable:
    def __init__(self, function: Callable, fake_return: Any = None):
        functools.update_wrapper(self, function)
        self.__function = function
        self.__fake_return = fake_return

    def __call__(self, *args, **kwargs):
        if config.DRYRUN:
            functionName = getattr(self.__function, "__name__", "UnknownFunction")

            logs.info(f"Dryable skip: Function {functionName} called with arguments {args} and keyword arguments {kwargs}", stacklevel=3)
            return self.__fake_return
        else:
            return self.__function(*args, **kwargs)

    def __get__(self, instance, owner):
        return functools.partial(self.__call__, instance)


def Dryable(function: Callable = None, fake_return: Any = None):
    if not function:
        def wrapper(function):
            return __Dryable(function, fake_return=fake_return)

        return wrapper
    else:
        return __Dryable(function)

