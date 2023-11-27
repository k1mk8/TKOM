
from lexer.interface import Lexer
from parser.interface import Parser
from tokkens.token import TokenType, Token, CONSTANT_TOKENS, Position
from parse_objects.objects import (
    Node,
    Program,
    FunctionDefinition,
    Block,
    Statement,
    IfStatement,
    WhileStatement,
    ReturnStatement,
    BreakStatement,
    ContinueStatement,
    VariableAccess,
    IdentifierExpression,
    FunctionCall,
    Assignment,
    Expression,
    OrExpression,
    AndExpression,
    Comparison,
    NegatedExpression,
    ExponentialExpression,
    Constant,
    TOKEN_TYPE_OPERATOR_MAPPING,
    ADDITIVE_OPERATOR_MAPPING,
    MULTIPLICATIVE_OPERATOR_MAPPING,
    BOOL_VALUE_MAPPING
)
from error_manager.interface import ErrorManager
from error_manager.parser_er import (
    UnexpectedToken,
    MissingSemiColon,
    ExpectingExpression,
    ExpectingIdentifier,
    MissingBracket,
    DuplicateDefinition
)


class Parser(Parser):
    def __init__(self, lexer, error_handler):
        self._error_handler = error_handler
        self._lexer = lexer
        self._token = None
        self._next_token()

    def parse(self):
        return self._parse_program()

    def _next_token(self):
        self._token = self._lexer.next()
        while self._token.type is TokenType.COMMENT:
            self._token = self._lexer.next()

    def _expect_object(self, method, method_name):
        if not (result := method()):
            error = UnexpectedToken(position=self._token.position, name=self._token.value, function_name=method_name)
            self._error_handler.fatal_error(error)
        return result

    def _parse_semi_colon(self):
        if self._token.type is not TokenType.SEMI_COLON:
            error = MissingSemiColon(position=self._token.position, name=self._token.value)
            if not self._error_handler.save_error(error):
                raise Exception('Error handler is full')
        else:
            self._next_token()

    def _parse_identifier(self):
        if self._token.type is not TokenType.ID:
            error = ExpectingIdentifier(position=self._token.position, name=self._token.value)
            self._error_handler.fatal_error(error)
        value = self._token.value
        self._next_token()
        return value

    def _parse_bracket(self, bracket_type):
        if self._token.type is not bracket_type:
            error = MissingBracket(position=self._token.position, name=bracket_type.value)
            if not self._error_handler.save_error(error):
                raise Exception('Error handler is full')
        else:
            self._next_token()

    def _parse_program(self):
        functions = self._parse_function_definitions()
        if self._token.type is not TokenType.EOF:
            error = UnexpectedToken(position=self._token.position, name=self._token.value)
            self._error_handler.fatal_error(error)
        return Program(position=Position(line=1, column=1), functions=functions)

    def _parse_function_definitions(self):
        functions = {}
        while self._token.type is TokenType.ID:
            position = self._token.position
            function_name = self._token.value
            self._next_token()
            self._parse_bracket(TokenType.ROUND_B_O)
            parameter_list = self._parse_parameter_list()
            self._parse_bracket(TokenType.ROUND_B_C)
            block = self._expect_object(self._parse_block, 'function_definitions')
            fun = FunctionDefinition(position=position, name=function_name, parameters=parameter_list, block=block)
            dict_fun = functions.setdefault(function_name, fun)
            if dict_fun != fun:
                error = DuplicateDefinition(position=position, name=function_name)
                self._error_handler.fatal_error(error)
        return functions
    
    def _parse_argument_list(self):
        arguments = []
        if not (node := self._parse_expression()):
            return []
        arguments.append(node)
        while self._token.type is TokenType.COMMA:
            self._next_token()
            node = self._expect_object(self._parse_expression, 'argument_list')
            arguments.append(node)
        return arguments

    def _parse_parameter_list(self):
        parameters = []
        position = self._token.position
        if self._token.type is not TokenType.ID:
            return []
        parameters.append(IdentifierExpression(position=position, name=self._token.value))
        self._next_token()
        while self._token.type is TokenType.COMMA:
            self._next_token()
            parameter_position = self._token.position
            name = self._parse_identifier()
            parameters.append(IdentifierExpression(position=parameter_position, name=name))
        return parameters

    def _parse_block(self):
        if self._token.type is not TokenType.BRACE_O:
            return
        position = self._token.position
        self._next_token()
        statement_list = self._parse_statement_list()
        self._parse_bracket(TokenType.BRACE_C)
        return Block(position=position, statements=statement_list)

    def _parse_statement_list(self):
        statements = []
        while statement := self._parse_statement():
            statements.append(statement)
        return statements

    def _parse_statement(self):
        statement = self._parse_variable_or_assignment() or \
            self._parse_if_statement() or \
            self._parse_while_statement() or \
            self._parse_return_statement() or \
            self._parse_break_statement() or \
            self._parse_continue_statement()
        return statement

    def _parse_variable_or_assignment(self):
        if not (variable_access := self._parse_variable_access()):
            return
        assignment = self._parse_assignment(left=variable_access)
        self._parse_semi_colon()
        return assignment or variable_access

    def _parse_variable_access(self):
        nodes = []
        position = self._token.position
        if not (node := self._parse_fun_call()):
            return
        nodes.append(node)
        while self._token.type is TokenType.DOT:
            self._next_token()
            node = self._expect_object(self._parse_fun_call, 'variable_access')
            nodes.append(node)
        return VariableAccess(position=position, variable=nodes)

    def _parse_assignment(self, left):
        if self._token.type is not TokenType.ASSIGN:
            return
        position = self._token.position
        self._next_token()
        expression = self._expect_object(self._parse_expression, 'assignment')
        return Assignment(position=position, left=left, right=expression)

    def _parse_fun_call(self):
        if self._token.type is not TokenType.ID:
            return
        position = self._token.position
        name = self._token.value
        self._next_token()
        if self._token.type is not TokenType.ROUND_B_O:
            expression = None
        else:
            self._next_token()
            expression = self._parse_argument_list()
            self._parse_bracket(TokenType.ROUND_B_C)
        if not expression and expression != []:
            return IdentifierExpression(name=name, position=position)
        return FunctionCall(name=name, position=position, arguments=expression)

    def _parse_if_statement(self):
        if self._token.type is not TokenType.IF_KEY:
            return
        position = self._token.position
        self._next_token()
        self._parse_bracket(TokenType.ROUND_B_O)
        condition = self._parse_expression()
        if not condition:
            error = UnexpectedToken(position=self._token.position, name=self._token.value)
            self._error_handler.fatal_error(error)
        self._parse_bracket(TokenType.ROUND_B_C)
        true_block = self._expect_object(self._parse_block, 'if_statement_true_block')
        if self._token.type is not TokenType.ELSE_KEY:
            return IfStatement(position=position, condition=condition, true_block=true_block)
        self._next_token()
        else_block = self._expect_object(self._parse_block, 'if_statement_else_block')
        return IfStatement(position=position, condition=condition, true_block=true_block, else_block=else_block)

    def _parse_while_statement(self):
        if self._token.type is not TokenType.WHILE_KEY:
            return
        position = self._token.position
        self._next_token()
        self._parse_bracket(TokenType.ROUND_B_O)
        condition = self._parse_expression()
        if not condition:
            error = UnexpectedToken(position=self._token.position, name=self._token.value)
            self._error_handler.fatal_error(error)
        self._parse_bracket(TokenType.ROUND_B_C)
        block = self._expect_object(self._parse_block, 'while_statement')
        return WhileStatement(position=position, condition=condition, true_block=block)

    def _parse_return_statement(self):
        if self._token.type is not TokenType.RETURN_KEY:
            return
        position = self._token.position
        self._next_token()
        expression = self._parse_expression()
        self._parse_semi_colon()
        return ReturnStatement(position=position, expression=expression)

    def _parse_break_statement(self):
        if self._token.type is not TokenType.BREAK_KEY:
            return
        position = self._token.position
        self._next_token()
        self._parse_semi_colon()
        return BreakStatement(position=position)

    def _parse_continue_statement(self):
        if self._token.type is not TokenType.CONTINUE_KEY:
            return
        position = self._token.position
        self._next_token()
        self._parse_semi_colon()
        return ContinueStatement(position=position)

    def _parse_expression(self):
        position = self._token.position
        if not (left := self._parse_or_operand()):
            return
        while self._token.type is TokenType.OR:
            self._next_token()
            right = self._expect_object(self._parse_or_operand, 'expression')
            left = OrExpression(position=position, left=left, right=right)
        return left

    def _parse_or_operand(self):
        position = self._token.position
        if not (left := self._parse_and_operand()):
            return
        while self._token.type is TokenType.AND:
            self._next_token()
            right = self._expect_object(self._parse_and_operand, 'or_operand')
            left = AndExpression(position=position, left=left, right=right)
        return left

    def _parse_and_operand(self):
        position = self._token.position
        negated = False
        if self._token.type is TokenType.NOT:
            negated = True
            self._next_token()
        node = self._parse_comparison()
        if negated and not node:
            error = ExpectingExpression(position=self._token.position, name=self._token.value)
            self._error_handler.fatal_error(error)
        if not negated and not node:
            return
        return NegatedExpression(position=position, left='!', right=node) if negated else node

    def _parse_comparison(self):
        position = self._token.position
        if not (left := self._parse_additive_expression()):
            return
        operator = TOKEN_TYPE_OPERATOR_MAPPING.get(self._token.type)
        if not operator:
            return left
        self._next_token()
        right = self._expect_object(self._parse_additive_expression, 'comparison')
        return Comparison(operator=operator, position=position, left=left, right=right)

    def _parse_additive_expression(self):
        position = self._token.position
        if not (left := self._parse_multiplicative_expression()):
            return
        while expression := ADDITIVE_OPERATOR_MAPPING.get(self._token.type):
            self._next_token()
            right = self._expect_object(self._parse_multiplicative_expression, 'additive_expression')
            left = expression(position=position, left=left, right=right)
        return left

    def _parse_multiplicative_expression(self):
        position = self._token.position
        if not (left := self._parse_factor()):
            return
        while expression := MULTIPLICATIVE_OPERATOR_MAPPING.get(self._token.type):
            self._next_token()
            right = self._expect_object(self._parse_factor, 'multiplicative_expression')
            left = expression(position=position, left=left, right=right)
        return left

    def _parse_factor(self):
        position = self._token.position
        if not (left := self._parse_exponent_factor()):
            return
        while self._token.type is TokenType.POWER or self._token.type is TokenType.TRANSFER:
            self._next_token()
            right = self._expect_object(self._parse_exponent_factor, 'factor')
            left = ExponentialExpression(position=position, left=left, right=right)
        return left

    def _parse_exponent_factor(self):
        position = self._token.position
        negated = False
        if self._token.type is TokenType.SUBTRACTION:
            negated = True
            self._next_token()
        node = self._parse_numeric_operand()
        if negated and not node:
            error = ExpectingExpression(position=self._token.position, name=self._token.value)
            self._error_handler.fatal_error(error)
        if not negated and not node:
            return
        return NegatedExpression(position=position, left='-', right=node) if negated else node


    def _parse_numeric_operand(self):
        operand = self._parse_constant() or \
            self._parse_bracket_expression() or \
            self._parse_variable_access()
        return operand

    def _parse_constant(self):
        if self._token.type not in CONSTANT_TOKENS:
            return
        bool_value = BOOL_VALUE_MAPPING.get(self._token.type)
        node = Constant(value=bool_value if bool_value is not None else self._token.value, position=self._token.position)
        self._next_token()
        return node

    def _parse_bracket_expression(self):
        if self._token.type is not TokenType.ROUND_B_O:
            return
        self._next_token()
        expression = self._expect_object(self._parse_expression, 'bracket_expression')
        self._parse_bracket(TokenType.ROUND_B_C)
        return expression

#
#This code is a parser for a simple programming language. It uses a lexer to tokenize the input code and then builds an abstract syntax tree (AST) by parsing the tokens. The parser handles errors and ensures that the input code follows the correct syntax.
#
#The parser is implemented as a class with methods for parsing different parts of the language, such as function definitions, blocks, statements, and expressions. Each method returns an AST node representing the parsed code.
#
#The parser uses a recursive descent parsing algorithm, which means it starts by parsing the highest-level construct (e.g., a function definition) and then recursively parses lower-level constructs (e.g., statements and expressions) within that construct.
#
#The parser also includes a lexer, which is responsible for tokenizing the input code. The lexer is implemented as a separate class and is used by the parser to obtain the next token to be parsed.
#
#The parser also includes an error manager, which is responsible for handling errors that occur during parsing. The error manager is implemented as a separate class and is used by the parser to report errors and terminate the parsing process if necessary.
#
#The parser is designed to be flexible and can be easily extended to support additional language features.