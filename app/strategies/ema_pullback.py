class EMAPullback:

    def bullish(self, close, ema20, tolerance=0.01):

        return abs(close - ema20) / ema20 <= tolerance

    def bearish(self, close, ema20, tolerance=0.01):

        return abs(close - ema20) / ema20 <= tolerance
