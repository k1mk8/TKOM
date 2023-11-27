
from abc import ABCMeta, abstractmethod


class Parser(metaclass=ABCMeta):
    """
    The Parser class is an abstract base class that provides a blueprint for creating parsers.
    """

    @abstractmethod
    def parse(self):
        """
        This method is used to parse the input and return a Node object.
        The Node object represents the structure of the parsed input.
        """
        ...