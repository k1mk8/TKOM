from typing import Any
from enum import StrEnum, auto
from dataclasses import dataclass


class TokenType(StrEnum):
    ID = auto()

    IF_KEY = auto()
    ELSE_KEY = auto()
    WHILE_KEY= auto()
    BREAK_KEY = auto()
    CONTINUE_KEY = auto()
    RETURN_KEY = auto()

    EQUAL = auto()
    GREATER = auto()
    SMALLER = auto()
    GREATER_EQ = auto()
    SMALLER_EQ = auto()
    NOT_EQ = auto()
    ASSIGN = auto()
    NOT = auto()
    AND = auto()
    OR = auto()
    ADD = auto()
    SUBTRACTION = auto()
    MULTIPLICATION = auto()
    DIVISION = auto()
    POWER = auto()
    TRANSFER = auto()

    INT = auto()
    FLOAT = auto()
    STR = auto()
    CURR = auto()

    BOOL_T = auto()
    BOOL_F = auto()

    ROUND_B_O = auto()
    ROUND_B_C = auto()
    BRACE_O = auto()
    BRACE_C = auto()
    COMMA = auto()
    DOT = auto()
    SEMI_COLON = auto()

    EOF = auto()
    COMMENT = auto()
    ERROR = auto()


KEY_MAPPING = {
    'if': TokenType.IF_KEY,
    'else': TokenType.ELSE_KEY,
    'while': TokenType.WHILE_KEY,
    'break': TokenType.BREAK_KEY,
    'continue': TokenType.CONTINUE_KEY,
    'return': TokenType.RETURN_KEY,
    'EUR' : TokenType.CURR,
    'PLN' : TokenType.CURR,
    'USD' : TokenType.CURR
}

SYMBOL_MAPPING = {
    '(': TokenType.ROUND_B_O,
    ')': TokenType.ROUND_B_C,
    '{': TokenType.BRACE_O,
    '}': TokenType.BRACE_C,
    ',': TokenType.COMMA,
    '.': TokenType.DOT,
    ';': TokenType.SEMI_COLON
}


OPERATOR_MAPPING = {
    '==': TokenType.EQUAL,
    '>': TokenType.GREATER,
    '<': TokenType.SMALLER,
    '>=': TokenType.GREATER_EQ,
    '<=': TokenType.SMALLER_EQ,
    '!=': TokenType.NOT_EQ,
    '=': TokenType.ASSIGN,
    '!': TokenType.NOT,
    '&&': TokenType.AND,
    '||': TokenType.OR,
    '+': TokenType.ADD,
    '-': TokenType.SUBTRACTION,
    '*': TokenType.MULTIPLICATION,
    '/': TokenType.DIVISION,
    '^': TokenType.POWER,
    '->': TokenType.TRANSFER
}

CONSTANT_TOKENS = [
    TokenType.INT,
    TokenType.FLOAT,
    TokenType.STR,
    TokenType.BOOL_T,
    TokenType.BOOL_F,
    TokenType.CURR
]

BOOL_MAPPING = {
    'true': TokenType.BOOL_T,
    'false': TokenType.BOOL_F
}

ESCAPE_CHARACTERS = {
    'n': b'\n',
    't': b'\t',
    'r': b'\r',
    'b': b'\b',
    '\\': b'\\'
}

@dataclass
class Position:
    line: int
    column: int

@dataclass
class Token:
    name: Any
    position: Position
    type: TokenType