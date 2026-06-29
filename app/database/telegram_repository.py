from .database import Database
from datetime import date


class TelegramRepository:

    def __init__(self):
        self.db = Database()

        self.db.execute("""
        CREATE TABLE IF NOT EXISTS telegram_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            signal TEXT,
            trade_date TEXT
        )
        """)

    def already_sent(self, symbol, signal):

        today = str(date.today())

        row = self.db.fetchone(
            """
            SELECT id
            FROM telegram_history
            WHERE symbol=? AND signal=? AND trade_date=?
            """,
            (symbol, signal, today)
        )

        return row is not None

    def mark_sent(self, symbol, signal):

        today = str(date.today())

        self.db.execute(
            """
            INSERT INTO telegram_history
            (symbol, signal, trade_date)
            VALUES (?, ?, ?)
            """,
            (symbol, signal, today)
        )
