class TradeValidator:

    def validate(self, trade):

        if trade.confidence < 90:

            return False

        if trade.quantity <= 0:

            return False

        if trade.entry <= trade.stop_loss:

            return False

        return True
