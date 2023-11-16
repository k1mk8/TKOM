import sys

from copy import copy

from lexer.interface import Lexer
from tokkens.token import (
    Token,
    TokenType,
    Position,
    SYMBOL_MAPPING,
    OPERATOR_MAPPING,
    BOOL_MAPPING,
    KEY_MAPPING,
    ESCAPE_CHARACTERS
)
from error_manager.lexer_er import (
    Overflow,
    StringTooLong,
    InfiniteString,
    UnknownTokens,
    NameTooLong,
    CommentTooLong,
    UnexpectedEscapeCharacter,
    TooLongLine
)


class Lexer(Lexer):
    token = None

    def __init__(self, source, error_handler, str_len_limit):
        self._source = source
        self._error_handler = error_handler
        self._str_len_limit = str_len_limit
        self._character = None
        self._current_position = Position(line=1, column=1)
        self._token_start_position = Position(line=1, column=1)
        self._newline_symbol = None
        self._next_character()

    def next(self):
        while self._character and self._character.isspace():
            self._next_character()
        self._token_start_position = copy(self._current_position)
        token = self._try_build_end_of_text() or \
            self._try_build_simple_token() or \
            self._try_build_number() or \
            self._try_build_identifier_or_keyword() or \
            self._try_build_comment() or \
            self._try_build_string() or \
            self._try_build_operator() or \
            self._try_build_unknown()
        return token

    def _next_character(self):
        if self._character == '\n':
            self._current_position.line += 1
            self._current_position.column = 1
        elif self._character:
            self._current_position.column += 1
        self._character = self._source.read(1)
        if self._character in ['\n', '\r']:
            if self._newline_symbol is None:
                newline_symbol = self._character
                potential_newline = self._source.read(1)
                if potential_newline in ['\n', '\r'] and newline_symbol + potential_newline in ['\r\n', '\n\r']:
                    self._newline_symbol = (newline_symbol + potential_newline).encode('utf-8')
                    self._character = '\n'
                    self._current_position.column = 1
                elif newline_symbol == '\n':
                    self._newline_symbol = '\n'.encode('utf-8')
                    self._source.seek(self._source.tell() - 1)
            else:
                newline_symbol = self._character
                if len(self._newline_symbol) == 2:
                    self._character = self._source.read(1)
                    newline_symbol += self._character

    def _try_build_end_of_text(self):
        if not self._character:
            return Token(value=None, position=self._token_start_position, type=TokenType.EOF)
        return None

    def _try_build_simple_token(self):
        type = SYMBOL_MAPPING.get(self._character, None)
        if not type:
            return None
        value = self._character
        self._next_character()
        return Token(value=value, position=self._token_start_position, type=type)

    def _try_build_number(self):
        if not self._character.isdecimal():
            return None
        error = None
        value = int(self._character)
        self._next_character()
        if value != 0:
            while self._character.isdecimal():
                decimal = int(self._character)
                if (sys.maxsize - decimal) / 10 - value > 0:
                    value = value * 10 + decimal
                else:
                    value = str(value)
                    while self._character.isdecimal() or self._character == '.':
                        value += self._character
                        self._next_character()
                    error = Overflow(position=self._token_start_position, name=value) #TODO
                    if not self._error_handler.save_error(error):
                        raise Exception('Error handler is full')
                    return Token(value=value, position=self._token_start_position, type=TokenType.ERROR)
                self._next_character()
        if not self._character == '.':
            return Token(value=value, position=self._token_start_position, type=TokenType.INT)
        number_of_decimals = 0
        fraction = 0
        self._next_character()
        while self._character.isdecimal():
            decimal = int(self._character)
            fraction = fraction * 10 + decimal
            number_of_decimals += 1
            self._next_character()
        value = value + fraction * pow(10, -number_of_decimals)
        return Token(value=value, position=self._token_start_position, type=TokenType.FLOAT)

    def _try_build_identifier_or_keyword(self):
        if not self._character.isalpha() and not self._character == '_':
            return None
        identifier = [self._character]
        self._next_character()
        while self._character and (self._character.isalnum() or self._character == '_'):
            if len(identifier) == self._str_len_limit:
                self._error_handling(identifier, 2)
                return Token(value=''.join(identifier), position=self._token_start_position, type=TokenType.COMMENT)
            identifier.append(self._character)
            self._next_character()
        identifier = ''.join(identifier)
        type = KEY_MAPPING.get(identifier, None) or BOOL_MAPPING.get(identifier, None) or TokenType.ID
        return Token(value=identifier, position=self._token_start_position, type=type)

    def _try_build_comment(self):
        if self._character == '#':
            value = []
            self._next_character()
            while self._character and self._character.encode() != self._newline_symbol:
                if len(value) == self._str_len_limit:
                    self._error_handling(value, 1)
                    return Token(value=''.join(value), position=self._token_start_position, type=TokenType.COMMENT)
                value.append(self._character)
                self._next_character()
            value = ''.join(value)
            return Token(value=value, position=self._token_start_position, type=TokenType.COMMENT)
        return None

    def _try_build_string(self):
        if self._character != '\'':
            return None
        literal = [''.encode()]
        error = None
        self._next_character()
        while self._character != '\'':
            if not self._character:
                error = InfiniteString(position=self._token_start_position, name=None)
                break
            if len(literal) == self._str_len_limit:
                self._error_handling(literal, 3)
                break
            escaped_character = None
            if self._character == '\\':
                self._next_character()
                escaped_character = ESCAPE_CHARACTERS.get(self._character, None)
            if escaped_character:
                literal.append(escaped_character)
            else:
                literal.append(self._character.encode())
            self._next_character()
        self._next_character()
        literal = b''.join(literal)
        if error:
            if not self._error_handler.save_error(error):
                raise Exception('Error handler is full')
        return Token(value=literal, position=self._token_start_position, type=TokenType.STR)

    def _try_build_operator(self):
        if self._character in ['+', '/', '*', '^']:
            operator = self._character
            operator_type = OPERATOR_MAPPING.get(operator, None)
            self._next_character()
            return Token(value=operator, position=self._token_start_position, type=operator_type)
        elif self._character in ['=', '>', '<', '!', '&', '|', '-']:
            operator = self._character
            self._next_character()
            operator = operator + self._character if self._character else operator
            operator_type = OPERATOR_MAPPING.get(operator, None)
            if operator_type:
                self._next_character()
                return Token(value=operator, position=self._token_start_position, type=operator_type)
            self._next_character()
            error = UnknownTokens(position=self._token_start_position, name=operator)
            if not self._error_handler.save_error(error):
                raise Exception('Error handler is full')
            return Token(value=operator, position=self._token_start_position, type=TokenType.ERROR)
        else:
            return None

    def _try_build_unknown(self):
        value = self._character
        error = UnknownTokens(position=self._token_start_position, name=value)
        if not self._error_handler.save_error(error):
            raise Exception('Error handler is full')
        self._next_character()
        return Token(value=value, position=self._token_start_position, type=TokenType.ERROR)
    
    def _error_handling(self, value, flag):
        if flag == 1:
            error = CommentTooLong(position=self._token_start_position, name=''.join(value[:20]))
        elif flag == 2:
            error = NameTooLong(position=self._token_start_position, name=''.join(value[:20]))
        elif flag == 3:
            error = StringTooLong(position=self._token_start_position, name=b''.join(value[:20]))
        if not self._error_handler.save_error(error):
            raise Exception('Error handler is full')
        loop_count = 0
        while self._character and self._character != '\'' and loop_count < 4 * self._str_len_limit:
            loop_count += 1
            self._next_character()
        if loop_count ==  4 * self._str_len_limit:
            error = TooLongLine(position=self._token_start_position, value=None)
            self._error_handler.fatal_error(error)
