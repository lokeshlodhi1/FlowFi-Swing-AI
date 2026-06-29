class DuplicateChecker:

    def __init__(self):

        self.sent = set()

    def already_sent(self, symbol):

        return symbol in self.sent

    def mark_sent(self, symbol):

        self.sent.add(symbol)
