class StopLossEngine:

    def atr(self, entry, atr, multiplier=1.5):

        return round(entry - atr * multiplier, 2)

    def swing(self, swing_low):

        return round(swing_low, 2)
