from error_manager.interface import Error

class NoMainFunction(Error):
    def __repr__(self) -> str:
        return '''The file does not contain the \'main\' function'''


class WrongTypeForOperation(Error):
    def __repr__(self) -> str:
        return f'''Operation between types {self.name[0]} and {self.name[1]} is not allowed
        in line {self.position.line}, column {self.position.column}'''
    
class BreakOrContinueOutsideWhile(Error):
    def __repr__(self) -> str:
        return f'''Break or continue outside the loop in function {self.name} in line {self.position.line}, 
        column {self.position.column}'''
    
class ValueSizeExceed(Error):
    def __repr__(self) -> str:
        return f'''Value size exceed in line {self.position.line}, column {self.position.column}'''


class DivisionByZero(Error):
    def __repr__(self) -> str:
        return f'''Division by zero try in line {self.position.line}, column {self.position.column}'''


class NotExactArguments(Error):
    def __repr__(self) -> str:
        return f'''Not exact number of arguments {self.name} in line {self.position[0].line}, column {self.position[0].column}.
        Calling on line {self.position[1].line}, column {self.position[1].column}
        '''


class UndefinedVariable(Error):
    def __repr__(self) -> str:
        return f'''No variable \'{self.name}\' in scope or not defined, in line {self.position.line}, column {self.position.column}'''


class FunctionNotFound(Error):
    def __repr__(self) -> str:
        return f'''Function not found \'{self.name}\', in line {self.position.line}, column {self.position.column}'''
