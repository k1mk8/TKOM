import sys

from lexer.lexer import Lexer
from parser.parser import Parser
from error_manager.error_manager import ModulErrorManager, FatalError
from visitor.interpreter_visitor import InterpreterVisitor


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Add path to file')
        sys.exit()
    with open(str(sys.argv[1]), 'r', newline='') as source_file, ModulErrorManager() as error_handler:
        try:
            lexer = Lexer(source=source_file, error_handler=error_handler, str_len_limit=256)
            parser = Parser(lexer=lexer, error_handler=error_handler)
            program = parser.parse()
            interpreter = InterpreterVisitor(error_handler)
            program.accept(interpreter)
        except FatalError:
            sys.exit()