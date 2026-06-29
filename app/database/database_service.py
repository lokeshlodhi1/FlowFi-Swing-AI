from .trade_repository import TradeRepository
from .signal_repository import SignalRepository
from .journal_repository import JournalRepository


class DatabaseService:

    def __init__(self):

        self.trades = TradeRepository()

        self.signals = SignalRepository()

        self.journal = JournalRepository()
