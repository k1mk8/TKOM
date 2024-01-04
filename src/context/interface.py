from abc import ABCMeta, abstractmethod
from typing import Any, Self, Optional, Union, Callable
from currency.currency import Currency


class ScopeTableInterface(metaclass=ABCMeta):
    parent_scope: Optional[Self]
    _table: dict[str, Union[Callable, int, float, bool, str, Currency]]

    @abstractmethod
    def insert_symbol(self, name, value):
        ...

    @abstractmethod
    def get_value(self, name):
        ...


class ContextInterface(metaclass=ABCMeta):
    _current_scope: ScopeTableInterface

    @abstractmethod
    def enter_scope(self):
        ...

    @abstractmethod
    def leave_scope(self):
        ...

    @abstractmethod
    def insert_symbol(self, name, value):
        ...

    @abstractmethod
    def get_value(self, name):
        ...
