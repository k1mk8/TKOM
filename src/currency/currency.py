from parse_objects.objects import Constant
from typing import Any
from dataclasses import dataclass

@dataclass
class Currency(Constant):
    symbol: Any