class TrendFilter:

    def bullish(self, ema20, ema50, ema200):

        return ema20 > ema50 > ema200

    def bearish(self, ema20, ema50, ema200):

        return ema20 < ema50 < ema200
