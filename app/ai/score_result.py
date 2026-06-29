from dataclasses import dataclass


@dataclass(slots=True)
class ScoreResult:

    total: int

    confidence: float

    signal: str

    passed: bool
