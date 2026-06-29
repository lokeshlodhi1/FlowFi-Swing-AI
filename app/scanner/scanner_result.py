from dataclasses import dataclass
from typing import List


@dataclass(slots=True)
class ScannerResult:

    symbol: str

    signal: str

    confidence: float

    entry: float

    stop_loss: float

    target1: float

    target2: float

    quantity: int

    reasons: List[str]

    passed: bool
