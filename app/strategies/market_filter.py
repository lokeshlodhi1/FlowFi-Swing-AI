class MarketFilter:

    def is_bullish(self, nifty_close, nifty_20ema):

        return nifty_close > nifty_20ema

    def is_bearish(self, nifty_close, nifty_20ema):

        return nifty_close < nifty_20ema
