from dataclasses import dataclass


@dataclass(slots=True)
class Portfolio:

    capital: float

    invested: float

    available: float

    unrealized_pnl: float

    realized_pnl: float

    total_trades: int

    open_positions: int
