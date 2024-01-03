from abc import ABCMeta, abstractmethod
from typing import Any, Self, Optional, Union, Callable


class ScopeTableInterface(metaclass=ABCMeta):
    parent_scope: Optional[Self]
    _table: dict[str, Union[Callable, int, float, bool, str]]

    @abstractmethod
    def insert_symbol(self, name: str, value: Any) -> None:
        ...

    @abstractmethod
    def get_value(self, name: str) -> Any:
        ...


class ContextInterface(metaclass=ABCMeta):
    _current_scope: ScopeTableInterface

    @abstractmethod
    def enter_scope(self) -> None:
        ...

    @abstractmethod
    def leave_scope(self) -> None:
        ...

    @abstractmethod
    def insert_symbol(self, name: str, value: Any) -> None:
        ...

    @abstractmethod
    def get_value(self, name: str) -> Any:
        ...
