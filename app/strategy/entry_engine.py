class EntryEngine:

    def buy(self, candle_high):

        return round(candle_high + 0.05, 2)

    def sell(self, candle_low):

        return round(candle_low - 0.05, 2)
