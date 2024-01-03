from error_manager.interface import Error

class NoMainFunction(Error):
    def __repr__(self) -> str:
        return '''The file does not contain the \'main\' function'''


class WrongTypeForOperation(Error):
    def __repr__(self) -> str:
        return f'''Operation between types {self.name[0]} and {self.name[1]} is not allowed
        in line {self.position.line}, column {self.position.column}'''


class DivisionByZero(Error):
    def __repr__(self) -> str:
        return f'''Division by zero try in line {self.position.line}, column {self.position.column}'''


class NotExactArguments(Error):
    def __repr__(self) -> str:
        return f'''Not exact number of arguments in line {self.position.line}, column {self.position.column}'''


class UndefinedVariable(Error):
    def __repr__(self) -> str:
        return f'''No variable \'{self.name}\' in scope or not defined, in line {self.position.line}, column {self.position.column}'''


class FunctionNotFound(Error):
    def __repr__(self) -> str:
        return f'''Function not found \'{self.name}\', in line {self.position.line}, column {self.position.column}'''
