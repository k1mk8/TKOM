from context.interface import ScopeTableInterface

class ScopeTable(ScopeTableInterface):
    def __init__(self, parent_scope = None):
        self.parent_scope = parent_scope
        self._table_function = {}
        self._table_variable = {}

    def insert_symbol_function(self, name, value):
        self._table_function[name] = value

    def insert_symbol_variable(self, name, value):
        self._table_variable[name] = value

    def get_value_function(self, name):
        return self._table_function.get(name)
    
    def get_value_variable(self, name):
        return self._table_variable.get(name)
