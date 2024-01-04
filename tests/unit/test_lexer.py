import pytest
import io

from lexer.lexer import Lexer
from tokkens.token import TokenType, Token, Position
from error_manager.error_manager import ModulErrorManager


class TestLexer:
    @pytest.mark.parametrize('source, expected_token', [
        ('', Token(value=None, position=Position(line=1, column=1), type=TokenType.EOF)),
        ('\n ', Token(value=None, position=Position(line=2, column=2), type=TokenType.EOF)),
        ('\r\n', Token(value=None, position=Position(line=2, column=1), type=TokenType.EOF)),
        ('\n\r', Token(value=None, position=Position(line=2, column=1), type=TokenType.EOF)),
        (' \n ', Token(value=None, position=Position(line=2, column=2), type=TokenType.EOF)),
        (' \r\n', Token(value=None, position=Position(line=2, column=1), type=TokenType.EOF)),
        (' \n\r', Token(value=None, position=Position(line=2, column=1), type=TokenType.EOF)),
        (' ', Token(value=None, position=Position(line=1, column=2), type=TokenType.EOF)),
        ('                   ', Token(value=None, position=Position(line=1, column=20), type=TokenType.EOF)),
        (' \n  \n\n\n   ', Token(value=None, position=Position(line=5, column=4), type=TokenType.EOF)),
    ])
    def test_next_EOF(self, source, expected_token):
        with ModulErrorManager() as error_handler:
            lexer = Lexer(source=io.StringIO(source, newline=''), error_handler=error_handler, str_len_limit=256)
            assert lexer.next() == expected_token

    @pytest.mark.parametrize('source, expected_token', [
        ('.', Token(value='.', position=Position(line=1, column=1), type=TokenType.DOT)),
        (',', Token(value=',', position=Position(line=1, column=1), type=TokenType.COMMA)),
        (';', Token(value=';', position=Position(line=1, column=1), type=TokenType.SEMI_COLON)),
        ('(', Token(value='(', position=Position(line=1, column=1), type=TokenType.ROUND_B_O)),
        (')', Token(value=')', position=Position(line=1, column=1), type=TokenType.ROUND_B_C)),
        ('{', Token(value='{', position=Position(line=1, column=1), type=TokenType.BRACE_O)),
        ('}', Token(value='}', position=Position(line=1, column=1), type=TokenType.BRACE_C)),
    ])
    def test_next_simple(self, source, expected_token):
        with ModulErrorManager() as error_handler:
            lexer = Lexer(source=io.StringIO(source, newline=''), error_handler=error_handler, str_len_limit=256)
            assert lexer.next() == expected_token

    @pytest.mark.parametrize('source, expected_token', [
        ('1', Token(value=1, position=Position(line=1, column=1), type=TokenType.INT)),
        (' 2', Token(value=2, position=Position(line=1, column=2), type=TokenType.INT)),
        (' \n 3', Token(value=3, position=Position(line=2, column=2), type=TokenType.INT)),
        ('44', Token(value=44, position=Position(line=1, column=1), type=TokenType.INT)),
        ('1234567', Token(value=1234567, position=Position(line=1, column=1), type=TokenType.INT)),
        ('1.23', Token(value=1.23, position=Position(line=1, column=1), type=TokenType.FLOAT)),
        ('123.456', Token(value=123.456, position=Position(line=1, column=1), type=TokenType.FLOAT)),
        ('0.0010', Token(value=0.001, position=Position(line=1, column=1), type=TokenType.FLOAT)),
        ('0.12', Token(value=0.12, position=Position(line=1, column=1), type=TokenType.FLOAT)),
    ])
    def test_next_number(self, source, expected_token):
        with ModulErrorManager() as error_handler:
            lexer = Lexer(source=io.StringIO(source, newline=''), error_handler=error_handler, str_len_limit=256)
            assert lexer.next() == expected_token

    @pytest.mark.parametrize('source, expected_token', [
        ('USD', Token(value='USD', position=Position(line=1, column=1), type=TokenType.CURR)),
        ('PLN', Token(value='PLN', position=Position(line=1, column=1), type=TokenType.CURR)),
        ('EUR', Token(value='EUR', position=Position(line=1, column=1), type=TokenType.CURR)),
        ('\n EUR', Token(value='EUR', position=Position(line=2, column=2), type=TokenType.CURR)),
    ])
    def test_next_curr(self, source, expected_token):
        with ModulErrorManager() as error_handler:
            lexer = Lexer(source=io.StringIO(source, newline=''), error_handler=error_handler, str_len_limit=256)
            assert lexer.next() == expected_token

    @pytest.mark.parametrize('source, expected_token', [
        ('ID', Token(value='ID', position=Position(line=1, column=1), type=TokenType.ID)),
        ('   test_identifier', Token(value='test_identifier', position=Position(line=1, column=4), type=TokenType.ID)),
        ('\n_id3nt1fier_123', Token(value='_id3nt1fier_123', position=Position(line=2, column=1), type=TokenType.ID)),
        ('\n\r_id3nt1fier_123', Token(value='_id3nt1fier_123', position=Position(line=2, column=1), type=TokenType.ID)),
        ('\n\n_id3nt1fier_123', Token(value='_id3nt1fier_123', position=Position(line=3, column=1), type=TokenType.ID)),
    ])
    def test_next_identifier(self, source, expected_token):
        with ModulErrorManager() as error_handler:
            lexer = Lexer(source=io.StringIO(source, newline=''), error_handler=error_handler, str_len_limit=256)
            assert lexer.next() == expected_token

    @pytest.mark.parametrize('source, expected_token', [
        ('if', Token(value='if', position=Position(line=1, column=1), type=TokenType.IF_KEY)),
        (' else', Token(value='else', position=Position(line=1, column=2), type=TokenType.ELSE_KEY)),
        (' \n while', Token(value='while', position=Position(line=2, column=2), type=TokenType.WHILE_KEY)),
        ('break', Token(value='break', position=Position(line=1, column=1), type=TokenType.BREAK_KEY)),
        ('continue',Token(value='continue', position=Position(line=1, column=1), type=TokenType.CONTINUE_KEY)),
        ('return', Token(value='return', position=Position(line=1, column=1), type=TokenType.RETURN_KEY)),
        ('\r\n return',Token(value='return', position=Position(line=2, column=2), type=TokenType.RETURN_KEY)),
    ])
    def test_next_keyword(self, source, expected_token):
        with ModulErrorManager() as error_handler:
            lexer = Lexer(source=io.StringIO(source, newline=''), error_handler=error_handler, str_len_limit=256)
            assert lexer.next() == expected_token

    @pytest.mark.parametrize('source, expected_token', [
        ('true', Token(value='true', position=Position(line=1, column=1), type=TokenType.BOOL_T)),
        (' false', Token(value='false', position=Position(line=1, column=2), type=TokenType.BOOL_F)),
        (' \n true', Token(value='true', position=Position(line=2, column=2), type=TokenType.BOOL_T)),
    ])
    def test_next_bool(self, source, expected_token):
        with ModulErrorManager() as error_handler:
            lexer = Lexer(source=io.StringIO(source, newline=''), error_handler=error_handler, str_len_limit=256)
            assert lexer.next() == expected_token

    @pytest.mark.parametrize('source, expected_token', [
        ('#', Token(value='', position=Position(line=1, column=1), type=TokenType.COMMENT)),
        (' #', Token(value='', position=Position(line=1, column=2), type=TokenType.COMMENT)),
        ('return#', Token(value='', position=Position(line=1, column=7), type=TokenType.COMMENT)),
        ('123#11', Token(value='11', position=Position(line=1, column=4), type=TokenType.COMMENT)),
        ('123\naaa#_test\n', Token(value='_test', position=Position(line=2, column=4), type=TokenType.COMMENT)),
    ])
    def test_next_comment(self, source, expected_token):
        with ModulErrorManager() as error_handler:
            lexer = Lexer(source=io.StringIO(source, newline=''), error_handler=error_handler, str_len_limit=256)
            tokens = []
            while True:
                token = lexer.next()
                tokens.append(token)
                if token.type is TokenType.EOF:
                    break
        assert expected_token in tokens

    @pytest.mark.parametrize('source, expected_token', [
        ('\'abc\'', Token(value=b'abc', position=Position(line=1, column=1), type=TokenType.STR)),
        ('\'aas21fdsas\'', Token(value=b'aas21fdsas', position=Position(line=1, column=1), type=TokenType.STR)),
        ('\'if\\nwhile\'', Token(value=b'if\nwhile', position=Position(line=1, column=1), type=TokenType.STR)),
        ('\'return\\\'\'', Token(value=b'return\'', position=Position(line=1, column=1), type=TokenType.STR)),
    ])
    def test_next_string(self, source, expected_token):
        with ModulErrorManager() as error_handler:
            lexer = Lexer(source=io.StringIO(source, newline=''), error_handler=error_handler, str_len_limit=256)
            token = lexer.next()
            assert token == expected_token

    @pytest.mark.parametrize('source, expected_token', [
        ('==', Token(value='==', position=Position(line=1, column=1), type=TokenType.EQUAL)),
        ('!=', Token(value='!=', position=Position(line=1, column=1), type=TokenType.NOT_EQ)),
        ('>', Token(value='>', position=Position(line=1, column=1), type=TokenType.GREATER)),
        ('<', Token(value='<', position=Position(line=1, column=1), type=TokenType.SMALLER)),
        ('>=', Token(value='>=', position=Position(line=1, column=1), type=TokenType.GREATER_EQ)),
        ('<=', Token(value='<=', position=Position(line=1, column=1), type=TokenType.SMALLER_EQ)),
        ('&&', Token(value='&&', position=Position(line=1, column=1), type=TokenType.AND)),
        ('||', Token(value='||', position=Position(line=1, column=1), type=TokenType.OR)),
        ('!', Token(value='!', position=Position(line=1, column=1), type=TokenType.NOT)),
        ('+', Token(value='+', position=Position(line=1, column=1), type=TokenType.ADD)),
        ('-', Token(value='-', position=Position(line=1, column=1), type=TokenType.SUBTRACTION)),
        ('*', Token(value='*', position=Position(line=1, column=1), type=TokenType.MULTIPLICATION)),
        ('/', Token(value='/', position=Position(line=1, column=1), type=TokenType.DIVISION)),
        ('^', Token(value='^', position=Position(line=1, column=1), type=TokenType.POWER)),
        ('=', Token(value='=', position=Position(line=1, column=1), type=TokenType.ASSIGN)),
        ('->', Token(value='->', position=Position(line=1, column=1), type=TokenType.TRANSFER)),
    ])
    def test_next_operator(self, source, expected_token):
        with ModulErrorManager() as error_handler:
            lexer = Lexer(source=io.StringIO(source, newline=''), error_handler=error_handler, str_len_limit=256)
            assert lexer.next() == expected_token

    @pytest.mark.parametrize('source, expected_token', [
        ('?', Token(value='?', position=Position(line=1, column=1), type=TokenType.ERROR)),
        ('[', Token(value='[', position=Position(line=1, column=1), type=TokenType.ERROR)),
        (']', Token(value=']', position=Position(line=1, column=1), type=TokenType.ERROR)),
        ('~', Token(value='~', position=Position(line=1, column=1), type=TokenType.ERROR)),
        ('"', Token(value='"', position=Position(line=1, column=1), type=TokenType.ERROR)),
        (':', Token(value=':', position=Position(line=1, column=1), type=TokenType.ERROR)),
    ])
    def test_next_unknown(self, source, expected_token):
        with ModulErrorManager() as error_handler:
            lexer = Lexer(source=io.StringIO(source, newline=''), error_handler=error_handler, str_len_limit=256)
            assert lexer.next() == expected_token

    @pytest.mark.parametrize('source, expected_character, expected_position', [
        ('aa', 'a', Position(line=1, column=2)),
        ('a ', ' ', Position(line=1, column=2)),
        ('  ', ' ', Position(line=1, column=2)),
        (' a', 'a', Position(line=1, column=2)),
        ('\n\n', '\n', Position(line=2, column=1)),
        ('\r\n', '', Position(line=2, column=1)),
        ('\n\r', '', Position(line=2, column=1)),
    ])
    def test_next_character(self, source, expected_character, expected_position):
        with ModulErrorManager() as error_handler:
            lexer = Lexer(source=io.StringIO(source, newline=''), error_handler=error_handler, str_len_limit=256)
            lexer._next_character()
            assert lexer._character == expected_character
            assert lexer._current_position == expected_position

    @pytest.mark.parametrize('source, expected_tokens', [
        ('gżegżółka\n if \'zadanie\'',
            [
                Token(value='gżegżółka', position=Position(line=1, column=1), type=TokenType.ID),
                Token(value='if', position=Position(line=2, column=2), type=TokenType.IF_KEY),
                Token(value=b'zadanie', position=Position(line=2, column=5), type=TokenType.STR),
                Token(value=None, position=Position(line=2, column=14), type=TokenType.EOF),
            ]),
        (
            'gżegżółka\r\n co_to \'string\' while',
            [
                Token(value='gżegżółka', position=Position(line=1, column=1), type=TokenType.ID),
                Token(value='co_to', position=Position(line=2, column=2), type=TokenType.ID),
                Token(value=b'string', position=Position(line=2, column=8), type=TokenType.STR),
                Token(value='while', position=Position(line=2, column=17), type=TokenType.WHILE_KEY),
                Token(value=None, position=Position(line=2, column=22), type=TokenType.EOF),
            ]
        ),
        (
            'gżegżółka\n\r while 24.5 PLN',
            [
                Token(value='gżegżółka', position=Position(line=1, column=1), type=TokenType.ID),
                Token(value='while', position=Position(line=2, column=2), type=TokenType.WHILE_KEY),
                Token(value=24.5, position=Position(line=2, column=8), type=TokenType.FLOAT),
                Token(value='PLN', position=Position(line=2, column=13), type=TokenType.CURR),
                Token(value=None, position=Position(line=2, column=16), type=TokenType.EOF),
            ]
        ),
    ])
    def test_next_bytes_before_newline(self, source, expected_tokens):
        with ModulErrorManager() as error_handler:
            lexer = Lexer(source=io.StringIO(source, newline=''), error_handler=error_handler, str_len_limit=256)
            tokens = []
            while True:
                token = lexer.next()
                tokens.append(token)
                if token.type is TokenType.EOF:
                    break
        assert expected_tokens == tokens
