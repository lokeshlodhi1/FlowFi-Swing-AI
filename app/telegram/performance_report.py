class PerformanceReport:

    def summary(self, trades):

        total = len(trades)

        wins = len(

            [

                t for t in trades

                if t.pnl > 0

            ]

        )

        losses = total - wins

        win_rate = 0

        if total:

            win_rate = wins / total * 100

        return {

            "Total Trades": total,

            "Wins": wins,

            "Losses": losses,

            "Win Rate": round(win_rate, 2)

        }
