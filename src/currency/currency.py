from parse_objects.objects import Constant
from typing import Any
from dataclasses import dataclass

@dataclass
class Currency(Constant):
    symbol: Any
    def __repr__(self):
        return f"{self.value} {self.symbol}"