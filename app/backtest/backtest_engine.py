from dataclasses import dataclass


@dataclass
class BacktestResult:

    total_trades: int

    winning_trades: int

    losing_trades: int

    win_rate: float

    total_profit: float

    average_profit: float

    average_loss: float

    profit_factor: float


class BacktestEngine:

    def __init__(self):

        self.trades = []

    def add_trade(

        self,

        entry,

        exit,

        quantity,

    ):

        pnl = (exit - entry) * quantity

        self.trades.append(pnl)

    def summary(self):

        total = len(self.trades)

        if total == 0:

            return BacktestResult(

                0,

                0,

                0,

                0,

                0,

                0,

                0,

                0,

            )

        wins = [

            x

            for x in self.trades

            if x > 0

        ]

        losses = [

            x

            for x in self.trades

            if x <= 0

        ]

        total_profit = sum(self.trades)

        gross_profit = sum(wins)

        gross_loss = abs(sum(losses))

        if gross_loss == 0:

            profit_factor = gross_profit

        else:

            profit_factor = round(

                gross_profit /

                gross_loss,

                2

            )

        return BacktestResult(

            total_trades=total,

            winning_trades=len(wins),

            losing_trades=len(losses),

            win_rate=round(

                len(wins)

                /

                total

                *

                100,

                2,

            ),

            total_profit=round(

                total_profit,

                2,

            ),

            average_profit=round(

                gross_profit /

                max(len(wins),1),

                2,

            ),

            average_loss=round(

                gross_loss /

                max(len(losses),1),

                2,

            ),

            profit_factor=profit_factor,

        )
