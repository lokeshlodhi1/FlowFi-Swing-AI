from dataclasses import dataclass


@dataclass
class PerformanceResult:

    total_trades: int

    wins: int

    losses: int

    win_rate: float

    total_profit: float

    total_loss: float

    net_profit: float

    profit_factor: float

    expectancy: float

    average_win: float

    average_loss: float


class PerformanceEngine:

    def __init__(self):

        self.trades = []

    def add_trade(

        self,

        pnl,

    ):

        self.trades.append(float(pnl))

    def calculate(self):

        if len(self.trades) == 0:

            return PerformanceResult(

                0,

                0,

                0,

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

        total_profit = sum(wins)

        total_loss = abs(sum(losses))

        net_profit = total_profit - total_loss

        if total_loss == 0:

            profit_factor = 999

        else:

            profit_factor = round(

                total_profit /

                total_loss,

                2,

            )

        win_rate = round(

            len(wins)

            /

            len(self.trades)

            *

            100,

            2,

        )

        average_win = round(

            total_profit /

            max(

                len(wins),

                1,

            ),

            2,

        )

        average_loss = round(

            total_loss /

            max(

                len(losses),

                1,

            ),

            2,

        )

        expectancy = round(

            (

                average_win

                *

                (

                    win_rate /

                    100

                )

            )

            -

            (

                average_loss

                *

                (

                    1

                    -

                    (

                        win_rate /

                        100

                    )

                )

            ),

            2,

        )

        return PerformanceResult(

            total_trades=len(self.trades),

            wins=len(wins),

            losses=len(losses),

            win_rate=win_rate,

            total_profit=round(

                total_profit,

                2,

            ),

            total_loss=round(

                total_loss,

                2,

            ),

            net_profit=round(

                net_profit,

                2,

            ),

            profit_factor=profit_factor,

            expectancy=expectancy,

            average_win=average_win,

            average_loss=average_loss,

        )