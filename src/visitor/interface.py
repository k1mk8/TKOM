from abc import abstractmethod, ABCMeta


class Visitor(metaclass=ABCMeta):
    ...


class Visitable(metaclass=ABCMeta):
    @abstractmethod
    def accept(visitor: type[Visitor]):
        ...