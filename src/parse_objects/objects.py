
from dataclasses import dataclass, field
from enum import StrEnum, auto
from typing import Any, Self, Optional, Callable

from tokkens.token import Position, TokenType


class Operator(StrEnum):
    EQ = auto()
    GT = auto()
    LT = auto()
    GE = auto()
    LE = auto()
    NE = auto()
    TR = auto()


TOKEN_TYPE_OPERATOR_MAPPING = {
    TokenType.EQUAL: Operator.EQ,
    TokenType.GREATER: Operator.GT,
    TokenType.SMALLER: Operator.LT,
    TokenType.GREATER_EQ: Operator.GE,
    TokenType.SMALLER_EQ: Operator.LE,
    TokenType.NOT_EQ: Operator.NE,
    TokenType.TRANSFER: Operator.TR
}


BOOL_VALUE_MAPPING = {
    TokenType.BOOL_T: True,
    TokenType.BOOL_F: False
}


@dataclass
class Node():
    position: Position


@dataclass
class Expression(Node):
    left: Self
    right: Self


class OrExpression(Expression):
    ...

class AndExpression(Expression):
    ...


@dataclass
class Comparison(Expression):
    operator: Operator


class NegatedExpression(Expression):
    ...


class AddExpression(Expression):
    ...


class SubExpression(Expression):
    ...


class MulExpression(Expression):
    ...


class DivExpression(Expression):
    ...


class ExponentialExpression(Expression):
    ...


@dataclass
class Constant(Node):
    value: Any


class Statement(Node):
    ...


@dataclass
class Block(Node):
    statements: list[Statement] = field(default_factory=lambda: [])


@dataclass
class IfStatement(Statement):
    condition: Expression
    true_block: Block
    else_block: Optional[Block] = None

@dataclass
class WhileStatement(Statement):
    condition: Expression
    true_block: Block


@dataclass
class ReturnStatement(Statement):
    expression: Optional[Expression] = None

class BreakStatement(Statement):
    ...


class ContinueStatement(Statement):
    ...


@dataclass
class VariableAccess(Statement):
    variable: list[Expression] = field(default_factory=lambda: [])


@dataclass
class Assignment(Statement):
    left: VariableAccess
    right: Expression

@dataclass
class IdentifierFunCall(Node):
    name: str


class IdentifierExpression(IdentifierFunCall):
    ...


@dataclass
class FunctionCall(IdentifierFunCall):
    arguments: list[Expression] = field(default_factory=lambda: [])


@dataclass
class FunctionDefinition(Node):
    name: str
    block: Block
    parameters: list[IdentifierExpression] = field(default_factory=lambda: [])


@dataclass
class Program(Node):
    functions: dict[str, FunctionDefinition]


ADDITIVE_OPERATOR_MAPPING = {
    TokenType.ADD: AddExpression,
    TokenType.SUBTRACTION: SubExpression
}


MULTIPLICATIVE_OPERATOR_MAPPING = {
    TokenType.MULTIPLICATION: MulExpression,
    TokenType.DIVISION: DivExpression
}

# In this code, we define a class hierarchy for an abstract syntax tree (AST) of a simple programming language. The AST represents the structure of the code and is used by the interpreter or compiler to analyze and execute the code.
#
# The `Node` class is the base class for all nodes in the AST. It has a `position that stores the position of the node in the source code.
#
# The `Expression` class is the base class for all expressions in the AST. It has `left` and `right` attributes that represent the left and right operands of the expression, respectively.
#
# The `Statement` class is the base class for all statements in the AST. It represents a unit of execution in the program.
#
# The `Block` class represents a sequence of statements. It has a `statements` attribute that is a list of statements in the block.
#
# The `Program` class represents the entire program. It has a` attribute that is a dictionary mapping function names to their definitions.
#
# The `FunctionDefinition` class represents a function definition. It has `name`, `block`, and `parameters` attributes that store the name of the function, its block of statements, and its parameters, respectively.
#
# The `FunctionCall` class represents a function call. It has a `name` attribute that stores the name of the function being called, and an `arguments` attribute that is a list of expressions representing the arguments passed to the function.
#
# The `IdentifierExpression` class represents an identifier expression. It has a `name` attribute that stores the name of the identifier.
#
# The `Constant` class represents a constant expression. It has a `value` attribute that stores the value of the constant.
#
# The `VariableAccess` class represents a variable access expression. It has a `variable` attribute that is a list of expressions representing the variable being accessed.
#
# The `Assignment` class represents an assignment statement. It has `left` and `right` attributes that represent the left and right operands of the assignment, respectively.
#
# The `ReturnStatement` class represents a return statement. It has an `expression` attribute that is an optional expression representing the value being returned by the function.
#
# The `IfStatement` class represents an if statement. It has `condition`, `true_block`, and `else_block` attributes that represent the condition of the if statement, the block of statements to be executed if the condition is true, and the block of statements to be executed if the condition is false, respectively.
#
# The `WhileStatement` class represents a while statement. It has `condition` and `true_block` attributes that represent the condition of the while statement and the block of statements to be executed while the condition is true, respectively.
#
# The `BreakStatement` and `ContinueStatement` classes represent break and continue statements, respectively.
#
# The `Operator` class is an enumeration that represents the various comparison operators in the language.