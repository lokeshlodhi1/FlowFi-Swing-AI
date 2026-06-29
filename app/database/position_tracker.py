class PositionTracker:

    def invested(self, trades):

        total = 0

        for trade in trades:

            total += trade.entry * trade.quantity

        return round(total, 2)

    def open_positions(self, trades):

        return len(trades)
