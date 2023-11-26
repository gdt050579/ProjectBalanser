
from abc import ABC
from typing import Generic, TypeVar

from .parse_error import ParseError
from utils import logs


T = TypeVar("T")

class Parser(Generic[T], ABC):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def _parse(self) -> T:
        raise NotImplementedError

    @logs.FunctionDebug
    def parse(self) -> T:
        try:
            return self._parse()
        except ParseError as error:
            logs.exception(f"Failed to parse {self.__class__.__name__} because of {error}")
            raise
        except Exception:
            logs.exception(f"Failed to parse {self.__class__.__name__} because of an unexpected exception.")
            raise

