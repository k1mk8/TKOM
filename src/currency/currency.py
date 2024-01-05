from parse_objects.objects import Constant
from typing import Any, Union
from dataclasses import dataclass

@dataclass
class Currency:
    value: Union[int, float]
    type: Any

    def __str__(self):
        return f'{self.value} {self.type}'