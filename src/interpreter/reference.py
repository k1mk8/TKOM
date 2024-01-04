from dataclasses import dataclass, field
from typing import Any, Self


@dataclass
class Reference:
    value: Any
    symbol: Any = None
    references: list[Self] = field(default_factory=lambda: [])