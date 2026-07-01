from app.scanner.strategies.pullback_strategy import PullbackStrategy
from app.scanner.strategies.breakout_strategy import BreakoutStrategy


class EntryEngine:

    def __init__(self, dataframe):

        self.df = dataframe

    def analyse(self):

        pullback = PullbackStrategy(self.df).scan()

        breakout = BreakoutStrategy(self.df).scan()

        strategies = []

        if pullback.valid:
            strategies.append(pullback)

        if breakout.valid:
            strategies.append(breakout)

        if len(strategies) == 0:

            return {

                "signal": "WATCH",

                "strategy": None,

                "reason": "No Valid Entry"

            }

        best = max(

            strategies,

            key=lambda x: x.confidence

        )

        return {

            "signal": best.reason,

            "strategy": best.setup,

            "confidence": best.confidence,

            "entry": best.entry,

            "stop_loss": best.stop_loss,

            "target1": best.target1,

            "target2": best.target2,

            "risk_reward": best.risk_reward

        }