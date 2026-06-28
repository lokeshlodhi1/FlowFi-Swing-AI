from dataclasses import dataclass

@dataclass
class Trade:

    stock: str

    signal: str

    entry: float

    stop: float

    target1: float

    target2: float

    quantity: int

    score: float
