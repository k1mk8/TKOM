from error_manager.interface import Error
    
class Overflow(Error):
    def __repr__(self):
        return f'Overflow in line {self.position.line}, column {self.position.column}'

class UnknownTokens(Error):
    def __repr__(self):
        return f'Unknown token {self.name} in line {self.position.line}, column {self.position.column}'
    
class StringTooLong(Error):
    def __repr__(self):
        return f'String too long in line {self.position.line}, column {self.position.column}'
    
class InfiniteString(Error):
    def __repr__(self):
        return f'String without end start in line {self.position.line}, column {self.position.column}'

class NameTooLong(Error):
    def __repr__(self):
        return f'Name {self.name} is too long in line {self.position.line}, column {self.position.column}'

class CommentTooLong(Error):
    def __repr__(self):
        return f'Name {self.name} is too long in line {self.position.line}, column {self.position.column}'       