import pytest

from parser.parser import Parser
from tokkens.token import TokenType, Token, Position
from parse_objects.objects import (
    Program,
    FunctionDefinition,
    Block,
    IfStatement,
    WhileStatement,
    ReturnStatement,
    BreakStatement,
    ContinueStatement,
    VariableAccess,
    IdentifierExpression,
    FunctionCall,
    OrExpression,
    AndExpression,
    Comparison,
    NegatedExpression,
    AddExpression,
    SubExpression,
    MulExpression,
    DivExpression,
    ExponentialExpression,
    Constant,
    Operator
)
from error_manager.error_manager import ModulErrorManager


class TestParser:

    @pytest.mark.parametrize('tokens, expected_tree', [
        (
            [
                Token(value='fun', position=Position(line=1, column=1), type=TokenType.ID),
                Token(value='(', position=Position(line=1, column=4), type=TokenType.ROUND_B_O),
                Token(value=')', position=Position(line=1, column=6), type=TokenType.ROUND_B_C),
                Token(value='{', position=Position(line=1, column=7), type=TokenType.BRACE_O),
                Token(value='}', position=Position(line=1, column=8), type=TokenType.BRACE_C),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            {
                'fun': FunctionDefinition(
                    position=Position(line=1, column=1),
                    name='fun',
                    parameters=[],
                    block=Block(position=Position(line=1, column=7), statements=[])
                )
            }
        ),
        (
            [
                Token(value='fun', position=Position(line=1, column=1), type=TokenType.ID),
                Token(value='(', position=Position(line=1, column=4), type=TokenType.ROUND_B_O),
                Token(value='x', position=Position(line=1, column=5), type=TokenType.ID),
                Token(value=')', position=Position(line=1, column=6), type=TokenType.ROUND_B_C),
                Token(value='{', position=Position(line=1, column=7), type=TokenType.BRACE_O),
                Token(value='}', position=Position(line=1, column=8), type=TokenType.BRACE_C),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            {
                'fun': FunctionDefinition(
                    position=Position(line=1, column=1),
                    name='fun',
                    parameters=[IdentifierExpression(position=Position(line=1, column=5), name='x')],
                    block=Block(position=Position(line=1, column=7), statements=[])
                )
            }
        ),
        (
            [
                Token(value='fun', position=Position(line=1, column=1), type=TokenType.ID),
                Token(value='(', position=Position(line=1, column=4), type=TokenType.ROUND_B_O),
                Token(value='x', position=Position(line=1, column=5), type=TokenType.ID),
                Token(value=',', position=Position(line=1, column=6), type=TokenType.COMMA),
                Token(value='y', position=Position(line=1, column=7), type=TokenType.ID),
                Token(value=')', position=Position(line=1, column=8), type=TokenType.ROUND_B_C),
                Token(value='{', position=Position(line=1, column=9), type=TokenType.BRACE_O),
                Token(value='}', position=Position(line=1, column=10), type=TokenType.BRACE_C),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            {
                'fun': FunctionDefinition(
                    position=Position(line=1, column=1),
                    name='fun',
                    parameters=[
                        IdentifierExpression(position=Position(line=1, column=5), name='x'),
                        IdentifierExpression(position=Position(line=1, column=7), name='y'),
                    ],
                    block=Block(position=Position(line=1, column=9), statements=[])
                )
            }
        ),
    ])
    def test_parse_function_definition(self, mocker, tokens, expected_tree):
        lexer = mocker.Mock()
        lexer.next.side_effect = tokens
        with ModulErrorManager() as error_handler:
            parser = Parser(lexer=lexer, error_handler=error_handler)
            functions = parser._parse_function_definitions()
            assert functions == expected_tree

    @pytest.mark.parametrize('tokens, expected_tree', [
        (
            [
                Token(value='x', position=Position(line=1, column=5), type=TokenType.ID),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            [IdentifierExpression(position=Position(line=1, column=5), name='x')],
        ),
        (
            [
                Token(value='x', position=Position(line=1, column=5), type=TokenType.ID),
                Token(value=',', position=Position(line=1, column=6), type=TokenType.COMMA),
                Token(value='y', position=Position(line=1, column=7), type=TokenType.ID),
                Token(value=',', position=Position(line=1, column=8), type=TokenType.COMMA),
                Token(value='z', position=Position(line=1, column=9), type=TokenType.ID),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            [
                IdentifierExpression(position=Position(line=1, column=5), name='x'),
                IdentifierExpression(position=Position(line=1, column=7), name='y'),
                IdentifierExpression(position=Position(line=1, column=9), name='z'),
            ]
        ),
    ])
    def test_parse_parameter_list(self, mocker, tokens, expected_tree):
        lexer = mocker.Mock()
        lexer.next.side_effect = tokens
        with ModulErrorManager() as error_handler:
            parser = Parser(lexer=lexer, error_handler=error_handler)
            assert parser._parse_parameter_list() == expected_tree

    @pytest.mark.parametrize('tokens, expected_tree', [
        (
            [
                Token(value='{', position=Position(line=1, column=5), type=TokenType.BRACE_O),
                Token(value='}', position=Position(line=1, column=6), type=TokenType.BRACE_C),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            Block(position=Position(line=1, column=5), statements=[])
        ),
        (
            [
                Token(value='{', position=Position(line=1, column=1), type=TokenType.BRACE_O),
                Token(value='break', position=Position(line=1, column=2), type=TokenType.BREAK_KEY),
                Token(value=';', position=Position(line=1, column=6), type=TokenType.SEMI_COLON),
                Token(value='}', position=Position(line=1, column=7), type=TokenType.BRACE_C),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            Block(position=Position(line=1, column=1), statements=[
                BreakStatement(position=Position(line=1, column=2))
            ])
        ),
        (
            [
                Token(value='{', position=Position(line=1, column=1), type=TokenType.BRACE_O),
                Token(value='object', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value='(', position=Position(line=1, column=8), type=TokenType.ROUND_B_O),
                Token(value=')', position=Position(line=1, column=9), type=TokenType.ROUND_B_C),
                Token(value=';', position=Position(line=1, column=10), type=TokenType.SEMI_COLON),
                Token(value='}', position=Position(line=1, column=11), type=TokenType.BRACE_C),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            Block(position=Position(line=1, column=1), statements=[
                VariableAccess(position=Position(line=1, column=2), variable=[
                    FunctionCall(
                        name='object',
                        position=Position(line=1, column=2),
                        arguments=[]
                    )
                ])
            ])
        ),
    ])
    def test_parse_block(self, mocker, tokens, expected_tree):
        lexer = mocker.Mock()
        lexer.next.side_effect = tokens
        with ModulErrorManager() as error_handler:
            parser = Parser(lexer=lexer, error_handler=error_handler)
            assert parser._parse_block() == expected_tree

    @pytest.mark.parametrize('tokens, expected_tree', [
        (
            [
                Token(value='a', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value='(', position=Position(line=1, column=8), type=TokenType.ROUND_B_O),
                Token(value=')', position=Position(line=1, column=9), type=TokenType.ROUND_B_C),
                Token(value=';', position=Position(line=1, column=10), type=TokenType.SEMI_COLON),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            FunctionCall(
                name='a',
                position=Position(line=1, column=2),
                arguments=[]
            )
        ),
        (
            [
                Token(value='a', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value=';', position=Position(line=1, column=6), type=TokenType.SEMI_COLON),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            IdentifierExpression(name='a', position=Position(line=1, column=2))
        ),
    ])
    def test_parse_fun_call(self, mocker, tokens, expected_tree):
        lexer = mocker.Mock()
        lexer.next.side_effect = tokens
        with ModulErrorManager() as error_handler:
            parser = Parser(lexer=lexer, error_handler=error_handler)
            assert parser._parse_fun_call() == expected_tree

    @pytest.mark.parametrize('tokens, expected_tree', [
        (
            [
                Token(value='if', position=Position(line=1, column=2), type=TokenType.IF_KEY),
                Token(value='(', position=Position(line=1, column=4), type=TokenType.ROUND_B_O),
                Token(value='x', position=Position(line=1, column=5), type=TokenType.ID),
                Token(value=')', position=Position(line=1, column=6), type=TokenType.ROUND_B_C),
                Token(value='{', position=Position(line=1, column=7), type=TokenType.BRACE_O),
                Token(value='}', position=Position(line=1, column=8), type=TokenType.BRACE_C),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            IfStatement(
                position=Position(line=1, column=2),
                condition=VariableAccess(position=Position(line=1, column=5), variable=[
                    IdentifierExpression(position=Position(line=1, column=5), name='x')
                ]),
                true_block=Block(position=Position(line=1, column=7), statements=[])
            )
        ),
        (
            [
                Token(value='if', position=Position(line=1, column=2), type=TokenType.IF_KEY),
                Token(value='(', position=Position(line=1, column=4), type=TokenType.ROUND_B_O),
                Token(value='x', position=Position(line=1, column=5), type=TokenType.ID),
                Token(value=')', position=Position(line=1, column=6), type=TokenType.ROUND_B_C),
                Token(value='{', position=Position(line=1, column=7), type=TokenType.BRACE_O),
                Token(value='}', position=Position(line=1, column=8), type=TokenType.BRACE_C),
                Token(value='else', position=Position(line=1, column=9), type=TokenType.ELSE_KEY),
                Token(value='{', position=Position(line=1, column=13), type=TokenType.BRACE_O),
                Token(value='}', position=Position(line=1, column=14), type=TokenType.BRACE_C),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            IfStatement(
                position=Position(line=1, column=2),
                condition=VariableAccess(position=Position(line=1, column=5), variable=[
                    IdentifierExpression(position=Position(line=1, column=5), name='x')
                ]),
                true_block=Block(position=Position(line=1, column=7), statements=[]),
                else_block=Block(position=Position(line=1, column=13), statements=[])
            )
        ),
    ])
    def test_parse_if_statement(self, mocker, tokens, expected_tree):
        lexer = mocker.Mock()
        lexer.next.side_effect = tokens
        with ModulErrorManager() as error_handler:
            parser = Parser(lexer=lexer, error_handler=error_handler)
            assert parser._parse_if_statement() == expected_tree

    @pytest.mark.parametrize('tokens, expected_tree', [
        (
            [
                Token(value='while', position=Position(line=1, column=2), type=TokenType.WHILE_KEY),
                Token(value='(', position=Position(line=1, column=4), type=TokenType.ROUND_B_O),
                Token(value='x', position=Position(line=1, column=5), type=TokenType.ID),
                Token(value=')', position=Position(line=1, column=6), type=TokenType.ROUND_B_C),
                Token(value='{', position=Position(line=1, column=7), type=TokenType.BRACE_O),
                Token(value='}', position=Position(line=1, column=8), type=TokenType.BRACE_C),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            WhileStatement(
                position=Position(line=1, column=2),
                condition=VariableAccess(position=Position(line=1, column=5), variable=[
                    IdentifierExpression(position=Position(line=1, column=5), name='x')
                ]),
                true_block=Block(position=Position(line=1, column=7), statements=[])
            )
        ),
    ])
    def test_parse_while_statement(self, mocker, tokens, expected_tree):
        lexer = mocker.Mock()
        lexer.next.side_effect = tokens
        with ModulErrorManager() as error_handler:
            parser = Parser(lexer=lexer, error_handler=error_handler)
            assert parser._parse_while_statement() == expected_tree

    @pytest.mark.parametrize('tokens, expected_tree', [
        (
            [
                Token(value='return', position=Position(line=1, column=2), type=TokenType.RETURN_KEY),
                Token(value=';', position=Position(line=1, column=6), type=TokenType.SEMI_COLON),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            ReturnStatement(position=Position(line=1, column=2))
        ),
        (
            [
                Token(value='return', position=Position(line=1, column=2), type=TokenType.RETURN_KEY),
                Token(value='x', position=Position(line=1, column=6), type=TokenType.ID),
                Token(value=';', position=Position(line=1, column=7), type=TokenType.SEMI_COLON),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            ReturnStatement(
                position=Position(line=1, column=2),
                expression=VariableAccess(
                    position=Position(line=1, column=6),
                    variable=[IdentifierExpression(position=Position(line=1, column=6), name='x')]
                )
            )
        ),
    ])
    def test_parse_return_statement(self, mocker, tokens, expected_tree):
        lexer = mocker.Mock()
        lexer.next.side_effect = tokens
        with ModulErrorManager() as error_handler:
            parser = Parser(lexer=lexer, error_handler=error_handler)
            assert parser._parse_return_statement() == expected_tree

    @pytest.mark.parametrize('tokens, expected_tree', [
        (
            [
                Token(value='break', position=Position(line=1, column=2), type=TokenType.BREAK_KEY),
                Token(value=';', position=Position(line=1, column=6), type=TokenType.SEMI_COLON),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            BreakStatement(position=Position(line=1, column=2))
        ),
    ])
    def test_parse_break_statement(self, mocker, tokens, expected_tree):
        lexer = mocker.Mock()
        lexer.next.side_effect = tokens
        with ModulErrorManager() as error_handler:
            parser = Parser(lexer=lexer, error_handler=error_handler)
            assert parser._parse_break_statement() == expected_tree

    @pytest.mark.parametrize('tokens, expected_tree', [
        (
            [
                Token(value='continue', position=Position(line=1, column=2), type=TokenType.CONTINUE_KEY),
                Token(value=';', position=Position(line=1, column=10), type=TokenType.SEMI_COLON),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            ContinueStatement(position=Position(line=1, column=2))
        ),
    ])
    def test_parse_continue_statement(self, mocker, tokens, expected_tree):
        lexer = mocker.Mock()
        lexer.next.side_effect = tokens
        with ModulErrorManager() as error_handler:
            parser = Parser(lexer=lexer, error_handler=error_handler)
            assert parser._parse_continue_statement() == expected_tree

    @pytest.mark.parametrize('tokens, expected_tree', [
        (
            [
                Token(value='x', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            VariableAccess(
                position=Position(line=1, column=2),
                variable=[IdentifierExpression(position=Position(line=1, column=2), name='x')]
            )
        ),
        (
            [
                Token(value='x', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            VariableAccess(
                position=Position(line=1, column=2),
                variable=[IdentifierExpression(position=Position(line=1, column=2), name='x')]
            )
        ),
        (
            [
                Token(value='x', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value='+', position=Position(line=1, column=3), type=TokenType.ADD),
                Token(value='y', position=Position(line=1, column=4), type=TokenType.ID),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            AddExpression(
                position=Position(line=1, column=2),
                left=VariableAccess(
                    position=Position(line=1, column=2),
                    variable=[IdentifierExpression(position=Position(line=1, column=2), name='x')]
                ),
                right=VariableAccess(
                    position=Position(line=1, column=4),
                    variable=[IdentifierExpression(position=Position(line=1, column=4), name='y')]
                )
            )
        ),
        (
            [
                Token(value='x', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value='+', position=Position(line=1, column=3), type=TokenType.ADD),
                Token(value=1, position=Position(line=1, column=4), type=TokenType.INT),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            AddExpression(
                position=Position(line=1, column=2),
                left=VariableAccess(
                    position=Position(line=1, column=2),
                    variable=[IdentifierExpression(position=Position(line=1, column=2), name='x')]
                ),
                right=Constant(position=Position(line=1, column=4), value=1)
            )
        ),
        (
            [
                Token(value=1.5, position=Position(line=1, column=2), type=TokenType.FLOAT),
                Token(value='+', position=Position(line=1, column=3), type=TokenType.ADD),
                Token(value=1, position=Position(line=1, column=4), type=TokenType.INT),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            AddExpression(
                position=Position(line=1, column=2),
                left=Constant(position=Position(line=1, column=2), value=1.5),
                right=Constant(position=Position(line=1, column=4), value=1)
            )
        ),
    ])
    def test_parse_add_expression(self, mocker, tokens, expected_tree):
        lexer = mocker.Mock()
        lexer.next.side_effect = tokens
        with ModulErrorManager() as error_handler:
            parser = Parser(lexer=lexer, error_handler=error_handler)
            assert parser._parse_expression() == expected_tree

    @pytest.mark.parametrize('tokens, expected_tree', [
        (
            [
                Token(value='x', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value='-', position=Position(line=1, column=3), type=TokenType.SUBTRACTION),
                Token(value='y', position=Position(line=1, column=4), type=TokenType.ID),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            SubExpression(
                position=Position(line=1, column=2),
                left=VariableAccess(
                    position=Position(line=1, column=2),
                    variable=[IdentifierExpression(position=Position(line=1, column=2), name='x')]
                ),
                right=VariableAccess(
                    position=Position(line=1, column=4),
                    variable=[IdentifierExpression(position=Position(line=1, column=4), name='y')]
                )
            )
        ),
        (
            [
                Token(value='x', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value='-', position=Position(line=1, column=3), type=TokenType.SUBTRACTION),
                Token(value=1, position=Position(line=1, column=4), type=TokenType.INT),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            SubExpression(
                position=Position(line=1, column=2),
                left=VariableAccess(
                    position=Position(line=1, column=2),
                    variable=[IdentifierExpression(position=Position(line=1, column=2), name='x')]
                ),
                right=Constant(position=Position(line=1, column=4), value=1)
            )
        ),
        (
            [
                Token(value=1.5, position=Position(line=1, column=2), type=TokenType.FLOAT),
                Token(value='-', position=Position(line=1, column=3), type=TokenType.SUBTRACTION),
                Token(value=1, position=Position(line=1, column=4), type=TokenType.INT),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            SubExpression(
                position=Position(line=1, column=2),
                left=Constant(position=Position(line=1, column=2), value=1.5),
                right=Constant(position=Position(line=1, column=4), value=1)
            )
        ),
    ])
    def test_parse_sub_expression(self, mocker, tokens, expected_tree):
        lexer = mocker.Mock()
        lexer.next.side_effect = tokens
        with ModulErrorManager() as error_handler:
            parser = Parser(lexer=lexer, error_handler=error_handler)
            assert parser._parse_expression() == expected_tree

    @pytest.mark.parametrize('tokens, expected_tree', [
        (
            [
                Token(value='x', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value='*', position=Position(line=1, column=3), type=TokenType.MULTIPLICATION),
                Token(value='y', position=Position(line=1, column=4), type=TokenType.ID),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            MulExpression(
                position=Position(line=1, column=2),
                left=VariableAccess(
                    position=Position(line=1, column=2),
                    variable=[IdentifierExpression(position=Position(line=1, column=2), name='x')]
                ),
                right=VariableAccess(
                    position=Position(line=1, column=4),
                    variable=[IdentifierExpression(position=Position(line=1, column=4), name='y')]
                )
            )
        ),
        (
            [
                Token(value='x', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value='*', position=Position(line=1, column=3), type=TokenType.MULTIPLICATION),
                Token(value=1, position=Position(line=1, column=4), type=TokenType.INT),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            MulExpression(
                position=Position(line=1, column=2),
                left=VariableAccess(
                    position=Position(line=1, column=2),
                    variable=[IdentifierExpression(position=Position(line=1, column=2), name='x')]
                ),
                right=Constant(position=Position(line=1, column=4), value=1)
            )
        ),
        (
            [
                Token(value=1.5, position=Position(line=1, column=2), type=TokenType.FLOAT),
                Token(value='*', position=Position(line=1, column=3), type=TokenType.MULTIPLICATION),
                Token(value=1, position=Position(line=1, column=4), type=TokenType.INT),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            MulExpression(
                position=Position(line=1, column=2),
                left=Constant(position=Position(line=1, column=2), value=1.5),
                right=Constant(position=Position(line=1, column=4), value=1)
            )
        ),
    ])
    def test_parse_mul_expression(self, mocker, tokens, expected_tree):
        lexer = mocker.Mock()
        lexer.next.side_effect = tokens
        with ModulErrorManager() as error_handler:
            parser = Parser(lexer=lexer, error_handler=error_handler)
            assert parser._parse_expression() == expected_tree

    @pytest.mark.parametrize('tokens, expected_tree', [
        (
            [
                Token(value='x', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value='/', position=Position(line=1, column=3), type=TokenType.DIVISION),
                Token(value='y', position=Position(line=1, column=4), type=TokenType.ID),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            DivExpression(
                position=Position(line=1, column=2),
                left=VariableAccess(
                    position=Position(line=1, column=2),
                    variable=[IdentifierExpression(position=Position(line=1, column=2), name='x')]
                ),
                right=VariableAccess(
                    position=Position(line=1, column=4),
                    variable=[IdentifierExpression(position=Position(line=1, column=4), name='y')]
                )
            )
        ),
        (
            [
                Token(value='x', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value='/', position=Position(line=1, column=3), type=TokenType.DIVISION),
                Token(value=1, position=Position(line=1, column=4), type=TokenType.INT),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            DivExpression(
                position=Position(line=1, column=2),
                left=VariableAccess(
                    position=Position(line=1, column=2),
                    variable=[IdentifierExpression(position=Position(line=1, column=2), name='x')]
                ),
                right=Constant(position=Position(line=1, column=4), value=1)
            )
        ),
        (
            [
                Token(value=1.5, position=Position(line=1, column=2), type=TokenType.FLOAT),
                Token(value='/', position=Position(line=1, column=3), type=TokenType.DIVISION),
                Token(value=1, position=Position(line=1, column=4), type=TokenType.INT),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            DivExpression(
                position=Position(line=1, column=2),
                left=Constant(position=Position(line=1, column=2), value=1.5),
                right=Constant(position=Position(line=1, column=4), value=1)
            )
        ),
    ])
    def test_parse_div_expression(self, mocker, tokens, expected_tree):
        lexer = mocker.Mock()
        lexer.next.side_effect = tokens
        with ModulErrorManager() as error_handler:
            parser = Parser(lexer=lexer, error_handler=error_handler)
            assert parser._parse_expression() == expected_tree

    @pytest.mark.parametrize('tokens, expected_tree', [
        (
            [
                Token(value='x', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value='^', position=Position(line=1, column=3), type=TokenType.POWER),
                Token(value='y', position=Position(line=1, column=4), type=TokenType.ID),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            ExponentialExpression(
                position=Position(line=1, column=2),
                left=VariableAccess(
                    position=Position(line=1, column=2),
                    variable=[IdentifierExpression(position=Position(line=1, column=2), name='x')]
                ),
                right=VariableAccess(
                    position=Position(line=1, column=4),
                    variable=[IdentifierExpression(position=Position(line=1, column=4), name='y')]
                )
            )
        ),
        (
            [
                Token(value='x', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value='^', position=Position(line=1, column=3), type=TokenType.POWER),
                Token(value=1, position=Position(line=1, column=4), type=TokenType.INT),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            ExponentialExpression(
                position=Position(line=1, column=2),
                left=VariableAccess(
                    position=Position(line=1, column=2),
                    variable=[IdentifierExpression(position=Position(line=1, column=2), name='x')]
                ),
                right=Constant(position=Position(line=1, column=4), value=1)
            )
        ),
        (
            [
                Token(value=1.5, position=Position(line=1, column=2), type=TokenType.FLOAT),
                Token(value='^', position=Position(line=1, column=3), type=TokenType.POWER),
                Token(value=1, position=Position(line=1, column=4), type=TokenType.INT),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            ExponentialExpression(
                position=Position(line=1, column=2),
                left=Constant(position=Position(line=1, column=2), value=1.5),
                right=Constant(position=Position(line=1, column=4), value=1)
            )
        ),
    ])
    def test_parse_pow_expression(self, mocker, tokens, expected_tree):
        lexer = mocker.Mock()
        lexer.next.side_effect = tokens
        with ModulErrorManager() as error_handler:
            parser = Parser(lexer=lexer, error_handler=error_handler)
            assert parser._parse_expression() == expected_tree

    @pytest.mark.parametrize('tokens, expected_tree', [
        (
            [
                Token(value='x', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value='&&', position=Position(line=1, column=3), type=TokenType.AND),
                Token(value='y', position=Position(line=1, column=4), type=TokenType.ID),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            AndExpression(
                position=Position(line=1, column=2),
                left=VariableAccess(
                    position=Position(line=1, column=2),
                    variable=[IdentifierExpression(position=Position(line=1, column=2), name='x')]
                ),
                right=VariableAccess(
                    position=Position(line=1, column=4),
                    variable=[IdentifierExpression(position=Position(line=1, column=4), name='y')]
                )
            )
        ),
        (
            [
                Token(value='x', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value='&&', position=Position(line=1, column=3), type=TokenType.AND),
                Token(value='true', position=Position(line=1, column=4), type=TokenType.BOOL_T),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            AndExpression(
                position=Position(line=1, column=2),
                left=VariableAccess(
                    position=Position(line=1, column=2),
                    variable=[IdentifierExpression(position=Position(line=1, column=2), name='x')]
                ),
                right=Constant(position=Position(line=1, column=4), value=True)
            )
        ),
    ])
    def test_parse_and_expression(self, mocker, tokens, expected_tree):
        lexer = mocker.Mock()
        lexer.next.side_effect = tokens
        with ModulErrorManager() as error_handler:
            parser = Parser(lexer=lexer, error_handler=error_handler)
            assert parser._parse_expression() == expected_tree

    @pytest.mark.parametrize('tokens, expected_tree', [
        (
            [
                Token(value='x', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value='||', position=Position(line=1, column=3), type=TokenType.OR),
                Token(value='y', position=Position(line=1, column=4), type=TokenType.ID),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            OrExpression(
                position=Position(line=1, column=2),
                left=VariableAccess(
                    position=Position(line=1, column=2),
                    variable=[IdentifierExpression(position=Position(line=1, column=2), name='x')]
                ),
                right=VariableAccess(
                    position=Position(line=1, column=4),
                    variable=[IdentifierExpression(position=Position(line=1, column=4), name='y')]
                )
            )
        ),
        (
            [
                Token(value='x', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value='||', position=Position(line=1, column=3), type=TokenType.OR),
                Token(value='true', position=Position(line=1, column=4), type=TokenType.BOOL_T),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            OrExpression(
                position=Position(line=1, column=2),
                left=VariableAccess(
                    position=Position(line=1, column=2),
                    variable=[IdentifierExpression(position=Position(line=1, column=2), name='x')]
                ),
                right=Constant(position=Position(line=1, column=4), value=True)
            )
        ),
    ])
    def test_parse_or_expression(self, mocker, tokens, expected_tree):
        lexer = mocker.Mock()
        lexer.next.side_effect = tokens
        with ModulErrorManager() as error_handler:
            parser = Parser(lexer=lexer, error_handler=error_handler)
            assert parser._parse_expression() == expected_tree

    @pytest.mark.parametrize('tokens, expected_tree', [
        (
            [
                Token(value='x', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value='!=', position=Position(line=1, column=3), type=TokenType.NOT_EQ),
                Token(value='y', position=Position(line=1, column=4), type=TokenType.ID),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            Comparison(
                position=Position(line=1, column=2),
                operator=Operator.NE,
                left=VariableAccess(
                    position=Position(line=1, column=2),
                    variable=[IdentifierExpression(position=Position(line=1, column=2), name='x')]
                ),
                right=VariableAccess(
                    position=Position(line=1, column=4),
                    variable=[IdentifierExpression(position=Position(line=1, column=4), name='y')]
                )
            )
        ),
        (
            [
                Token(value='x', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value='==', position=Position(line=1, column=3), type=TokenType.EQUAL),
                Token(value=1, position=Position(line=1, column=4), type=TokenType.INT),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            Comparison(
                position=Position(line=1, column=2),
                operator=Operator.EQ,
                left=VariableAccess(
                    position=Position(line=1, column=2),
                    variable=[IdentifierExpression(position=Position(line=1, column=2), name='x')]
                ),
                right=Constant(position=Position(line=1, column=4), value=1)
            )
        ),
        (
            [
                Token(value=1.5, position=Position(line=1, column=2), type=TokenType.FLOAT),
                Token(value='>', position=Position(line=1, column=3), type=TokenType.GREATER),
                Token(value=1, position=Position(line=1, column=4), type=TokenType.INT),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            Comparison(
                position=Position(line=1, column=2),
                operator=Operator.GT,
                left=Constant(position=Position(line=1, column=2), value=1.5),
                right=Constant(position=Position(line=1, column=4), value=1)
            )
        ),
    ])
    def test_parse_comparison(self, mocker, tokens, expected_tree):
        lexer = mocker.Mock()
        lexer.next.side_effect = tokens
        with ModulErrorManager() as error_handler:
            parser = Parser(lexer=lexer, error_handler=error_handler)
            assert parser._parse_expression() == expected_tree

    @pytest.mark.parametrize('tokens, expected_tree', [
        (
            [
                Token(value='!', position=Position(line=1, column=3), type=TokenType.NOT),
                Token(value='y', position=Position(line=1, column=4), type=TokenType.ID),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            NegatedExpression(
                position=Position(line=1, column=3),
                left='!',
                right=VariableAccess(
                    position=Position(line=1, column=4),
                    variable=[IdentifierExpression(position=Position(line=1, column=4), name='y')]
                )
            )
        ),
        (
            [
                Token(value='!', position=Position(line=1, column=3), type=TokenType.NOT),
                Token(value='false', position=Position(line=1, column=4), type=TokenType.BOOL_F),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            NegatedExpression(
                position=Position(line=1, column=3),
                left='!',
                right=Constant(position=Position(line=1, column=4), value=False)
            )
        ),
        (
            [
                Token(value='-', position=Position(line=1, column=3), type=TokenType.SUBTRACTION),
                Token(value=1, position=Position(line=1, column=4), type=TokenType.INT),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            NegatedExpression(
                position=Position(line=1, column=3),
                left='-',
                right=Constant(position=Position(line=1, column=4), value=1)
            )
        ),
    ])
    def test_parse_negated_expression(self, mocker, tokens, expected_tree):
        lexer = mocker.Mock()
        lexer.next.side_effect = tokens
        with ModulErrorManager() as error_handler:
            parser = Parser(lexer=lexer, error_handler=error_handler)
            assert parser._parse_expression() == expected_tree

    @pytest.mark.parametrize('tokens, expected_tree', [
        (
            [
                Token(value='x', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value='&&', position=Position(line=1, column=3), type=TokenType.AND),
                Token(value='y', position=Position(line=1, column=4), type=TokenType.ID),
                Token(value='||', position=Position(line=1, column=5), type=TokenType.OR),
                Token(value='z', position=Position(line=1, column=6), type=TokenType.ID),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            OrExpression(
                position=Position(line=1, column=2),
                left=AndExpression(
                    position=Position(line=1, column=2),
                    left=VariableAccess(
                        position=Position(line=1, column=2),
                        variable=[IdentifierExpression(position=Position(line=1, column=2), name='x')]
                    ),
                    right=VariableAccess(
                        position=Position(line=1, column=4),
                        variable=[IdentifierExpression(position=Position(line=1, column=4), name='y')]
                    ),
                ),
                right=VariableAccess(
                    position=Position(line=1, column=6),
                    variable=[IdentifierExpression(position=Position(line=1, column=6), name='z')]
                )
            )
        ),
        (
            [
                Token(value='x', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value='&&', position=Position(line=1, column=3), type=TokenType.AND),
                Token(value='(', position=Position(line=1, column=4), type=TokenType.ROUND_B_O),
                Token(value='y', position=Position(line=1, column=5), type=TokenType.ID),
                Token(value='||', position=Position(line=1, column=6), type=TokenType.OR),
                Token(value='z', position=Position(line=1, column=7), type=TokenType.ID),
                Token(value=')', position=Position(line=1, column=8), type=TokenType.ROUND_B_C),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            AndExpression(
                position=Position(line=1, column=2),
                right=OrExpression(
                    position=Position(line=1, column=5),
                    right=VariableAccess(
                        position=Position(line=1, column=7),
                        variable=[IdentifierExpression(position=Position(line=1, column=7), name='z')]
                    ),
                    left=VariableAccess(
                        position=Position(line=1, column=5),
                        variable=[IdentifierExpression(position=Position(line=1, column=5), name='y')]
                    ),
                ),
                left=VariableAccess(
                    position=Position(line=1, column=2),
                    variable=[IdentifierExpression(position=Position(line=1, column=2), name='x')]
                )
            )
        ),
        (
            [
                Token(value='x', position=Position(line=1, column=1), type=TokenType.ID),
                Token(value='&&', position=Position(line=1, column=2), type=TokenType.AND),
                Token(value='!', position=Position(line=1, column=3), type=TokenType.NOT),
                Token(value='(', position=Position(line=1, column=4), type=TokenType.ROUND_B_O),
                Token(value='y', position=Position(line=1, column=5), type=TokenType.ID),
                Token(value='||', position=Position(line=1, column=6), type=TokenType.OR),
                Token(value='z', position=Position(line=1, column=7), type=TokenType.ID),
                Token(value=')', position=Position(line=1, column=8), type=TokenType.ROUND_B_C),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            AndExpression(
                position=Position(line=1, column=1),
                right=NegatedExpression(
                    position=Position(line=1, column=3),
                    left='!',
                    right=OrExpression(
                        position=Position(line=1, column=5),
                        right=VariableAccess(
                            position=Position(line=1, column=7),
                            variable=[IdentifierExpression(position=Position(line=1, column=7), name='z')]
                        ),
                        left=VariableAccess(
                            position=Position(line=1, column=5),
                            variable=[IdentifierExpression(position=Position(line=1, column=5), name='y')]
                        ),
                    )
                ),
                left=VariableAccess(
                    position=Position(line=1, column=1),
                    variable=[IdentifierExpression(position=Position(line=1, column=1), name='x')]
                )
            )
        ),
    ])
    def test_parse_complex_expression(self, mocker, tokens, expected_tree):
        lexer = mocker.Mock()
        lexer.next.side_effect = tokens
        with ModulErrorManager() as error_handler:
            parser = Parser(lexer=lexer, error_handler=error_handler)
            assert parser._parse_expression() == expected_tree

    @pytest.mark.parametrize('tokens, expected_tree', [
        (
            [
                Token(value='x', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value='->', position=Position(line=1, column=3), type=TokenType.TRANSFER),
                Token(value='y', position=Position(line=1, column=4), type=TokenType.ID),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            ExponentialExpression(
                position=Position(line=1, column=2),
                left=VariableAccess(
                    position=Position(line=1, column=2),
                    variable=[IdentifierExpression(position=Position(line=1, column=2), name='x')]
                ),
                right=VariableAccess(
                    position=Position(line=1, column=4),
                    variable=[IdentifierExpression(position=Position(line=1, column=4), name='y')]
                )
            )
        ),
        (
            [
                Token(value='x', position=Position(line=1, column=2), type=TokenType.ID),
                Token(value='->', position=Position(line=1, column=3), type=TokenType.TRANSFER),
                Token(value='USD', position=Position(line=1, column=4), type=TokenType.CURR),
                Token(value=None, position=Position(line=1, column=34), type=TokenType.EOF),
            ],
            ExponentialExpression(
                position=Position(line=1, column=2),
                left=VariableAccess(
                    position=Position(line=1, column=2),
                    variable=[IdentifierExpression(position=Position(line=1, column=2), name='x')]
                ),
                right=Constant(position=Position(line=1, column=4), value='USD')
            )
        ),
    ])
    def test_parse_transfer_operator(self, mocker, tokens, expected_tree):
        lexer = mocker.Mock()
        lexer.next.side_effect = tokens
        with ModulErrorManager() as error_handler:
            parser = Parser(lexer=lexer, error_handler=error_handler)
            assert parser._parse_expression() == expected_tree
