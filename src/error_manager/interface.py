from abc import abstractmethod
from contextlib import AbstractContextManager
from dataclasses import dataclass
from typing import Any
from tokkens.token import Position

@dataclass
class Error:
    position: Position
    name: Any

class FatalError(Exception):
    ...

class ErrorManager(AbstractContextManager):
    @abstractmethod
    def save_error(self, error: type[Error]):
        ...

    @abstractmethod
    def fatal_error(self, error: type[Error]):
        ...