
from abc import ABCMeta, abstractmethod


class Lexer(metaclass=ABCMeta):
    """
    The Lexer class is an abstract base class that provides a blueprint for creating lexers.
    A lexer is a program that reads a sequence of characters and converts them into a sequence of tokens.
    """

    @abstractmethod
    def next(self):
        """
        The next method is an abstract method that must be implemented by any concrete subclass of Lexer.
        This method should return the next token in the sequence.
        """
        ...