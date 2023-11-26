
from abc import ABC
from typing import Generic, TypeVar

from .fix_error import FixError
from utils import logs


T = TypeVar("T")

class Fixer(Generic[T], ABC):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def _fix(self) -> T:
        raise NotImplementedError

    @logs.FunctionDebug
    def fix(self) -> T:
        try:
            return self._fix()
        except FixError as error:
            logs.exception(f"Failed to fix {self.__class__.__name__} because of {error}")
            raise
        except Exception:
            logs.exception(f"Failed to fix {self.__class__.__name__} because of an unexpected exception.")
            raise

