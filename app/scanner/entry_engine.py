from app.scanner.strategies.pullback_strategy import PullbackStrategy
from app.scanner.strategies.breakout_strategy import BreakoutStrategy
from app.scanner.strategies.vcp_strategy import VCPStrategy


class EntryEngine:

    def __init__(self, dataframe):

        self.df = dataframe

    def analyse(self):

        strategies = []

        # -----------------------------------
        # Pullback Strategy
        # -----------------------------------

        pullback = PullbackStrategy(self.df).scan()

        if pullback.valid:
            strategies.append(pullback)

        # -----------------------------------
        # Breakout Strategy
        # -----------------------------------

        breakout = BreakoutStrategy(self.df).scan()

        if breakout.valid:
            strategies.append(breakout)

        # -----------------------------------
        # VCP Strategy
        # -----------------------------------

        vcp = VCPStrategy(self.df).scan()

        if vcp.valid:
            strategies.append(vcp)

        # -----------------------------------
        # No Valid Strategy
        # -----------------------------------

        if not strategies:

            return {
                "signal": "WATCH",
                "strategy": None,
                "confidence": 0,
                "entry": 0,
                "stop_loss": 0,
                "target1": 0,
                "target2": 0,
                "risk_reward": 0,
                "reason": "No Valid Entry",
            }

        # -----------------------------------
        # Select Best Strategy
        # -----------------------------------

        best = max(strategies, key=lambda strategy: strategy.confidence)

        return {

            "signal": "BUY" if best.valid else "WATCH",

            "strategy": best.setup,

            "confidence": best.confidence,

            "entry": best.entry,

            "stop_loss": best.stop_loss,

            "target1": best.target1,

            "target2": best.target2,

            "risk_reward": best.risk_reward,

            "reason": best.reason,

        }