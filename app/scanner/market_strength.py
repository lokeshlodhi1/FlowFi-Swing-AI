class MarketStrength:

    def score(self, close, ema20):

        if close > ema20 * 1.03:
            return "STRONG_BULL"

        if close > ema20:
            return "BULL"

        if close < ema20 * 0.97:
            return "STRONG_BEAR"

        return "SIDEWAYS"
