from .database import Database
from .models import (
    TRADE_TABLE,
    SIGNAL_TABLE,
    JOURNAL_TABLE
)


class Repository:

    def __init__(self):

        self.db = Database()

        self.create_tables()

    def create_tables(self):

        self.db.execute(TRADE_TABLE)

        self.db.execute(SIGNAL_TABLE)

        self.db.execute(JOURNAL_TABLE)
