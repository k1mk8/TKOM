from error_manager.interface import Error

class UnexpectedToken(Error):
    def __repr__(self):
        return f'Unexpected token {self.name} in line {self.position.line}, column {self.position.column}'
    
class DuplicateDefinition(Error):
    def __repr__(self):
        return f'Duplicate name {self.name} in line {self.position.line}, column {self.position.column}'
    
class ExpectingIdentifier(Error):
    def __repr__(self):
        return f'Expecting identifier in line {self.position.line}, column {self.position.column}'
    
class ExpectingExpression(Error):
    def __repr__(self):
        return f'Expecting expression in line {self.position.line}, column {self.position.column}'
    
class MissingSemiColon(Error):
    def __repr__(self):
        return f'Missing semi-colon in line {self.position.line}, column {self.position.column}'
    
class MissingBracket(Error):
    def __repr__(self):
        return f'Missing bracket in line {self.position.line}, column {self.position.column}'