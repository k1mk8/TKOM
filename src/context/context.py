from context.interface import ContextInterface
from context.scope import ScopeTable


class Context(ContextInterface):
    def __init__(self, global_context = None):
        self._current_scope = ScopeTable()
        self._global_context = global_context

    def enter_scope(self):
        new_scope = ScopeTable(self._current_scope)
        self._current_scope = new_scope

    def leave_scope(self):
        old_scope = self._current_scope
        self._current_scope = self._current_scope.parent_scope
        del old_scope

    def insert_symbol_function(self, name, value):
        self._current_scope.insert_symbol_function(name, value)

    def insert_symbol_variable(self, name, value):
        self._current_scope.insert_symbol_variable(name, value)

    def get_value_function(self, name):
        value = self._current_scope.get_value_function(name)
        if value is not None:
            return value
        outer_scope = self._current_scope.parent_scope
        while outer_scope:
            value = outer_scope.get_value_function(name)
            if value is not None:
                return value
            outer_scope = outer_scope.parent_scope
        value = self._global_context.get_value_function(name) if self._global_context else None
        if value is not None:
            return value
        
    def get_value_variable(self, name):
        value = self._current_scope.get_value_variable(name)
        if value is not None:
            return value
        outer_scope = self._current_scope.parent_scope
        while outer_scope:
            value = outer_scope.get_value_variable(name)
            if value is not None:
                return value
            outer_scope = outer_scope.parent_scope
        value = self._global_context.get_value_variable(name) if self._global_context else None
        if value is not None:
            return value
