
import io

import pytest

from lexer.lexer import Lexer
from parser.parser import Parser
from tokkens.token import Position
from parse_objects.objects import (
    Program,
    IfStatement,
    FunctionDefinition,
    Block,
    IdentifierExpression,
    VariableAccess,
    Constant
)
from error_manager.error_manager import ModulErrorManager


class TestLexerParser:
    @pytest.mark.parametrize('source, expected_tree', [
        (
            'fun(){}',
            Program(position=Position(line=1, column=1), functions={
                'fun': FunctionDefinition(
                    position=Position(line=1, column=1),
                    name='fun',
                    parameters=[],
                    block=Block(position=Position(line=1, column=6), statements=[])
                )
            })
        ),
        (
            'fun(x){}',
            Program(position=Position(line=1, column=1), functions={
                'fun': FunctionDefinition(
                    position=Position(line=1, column=1),
                    name='fun',
                    parameters=[IdentifierExpression(position=Position(line=1, column=5), name='x')],
                    block=Block(position=Position(line=1, column=7), statements=[])
                )
            })
        ),
        (
            'fun(x, y, z){}',
            Program(position=Position(line=1, column=1), functions={
                'fun': FunctionDefinition(
                    position=Position(line=1, column=1),
                    name='fun',
                    parameters=[
                        IdentifierExpression(position=Position(line=1, column=5), name='x'),
                        IdentifierExpression(position=Position(line=1, column=8), name='y'),
                        IdentifierExpression(position=Position(line=1, column=11), name='z'),
                    ],
                    block=Block(position=Position(line=1, column=13), statements=[])
                )
            })
        ),
    ])
    def test_function_definition(self, source, expected_tree):
        with ModulErrorManager() as error_handler:
            lexer = Lexer(source=io.StringIO(source, newline=''), error_handler=error_handler, str_len_limit=256)
            parser = Parser(lexer=lexer, error_handler=error_handler)
        assert parser.parse() == expected_tree

#
#In this code, we have a class `TestLexerParser` with a method `test_function_definition`. This method uses the `pytest.mark.parametrize` decorator to run the test with different inputs.
#
#The `source` parameter represents the input code, and the `expected_tree` parameter represents the expected output of the parser.
#
#The test uses a `ModulErrorManager` context manager to handle errors during lexing and parsing.
#
#The `Lexer` class is used to tokenize the input code, and the `Parser` class is used to parse the tokens into an abstract syntax tree (AST).
#
#The `assert` statement at the end of the test checks if the output of the parser matches the expected output.
#
#This test ensures that the parser can correctly parse function definitions with different numbers of parameters..</s>