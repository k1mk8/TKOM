from abc import ABCMeta, abstractmethod


class Lexer(metaclass=ABCMeta):
    @abstractmethod
    def next(self):
        ...
