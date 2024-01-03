from context.interface import ScopeTableInterface

class ScopeTable(ScopeTableInterface):
    def __init__(self, parent_scope = None):
        self.parent_scope = parent_scope
        self._table = {}

    def insert_symbol(self, name, value):
        self._table[name] = value

    def get_value(self, name):
        return self._table.get(name)
