from .database import Database


class TradeRepository:

    def __init__(self):

        self.db = Database()

    def add_trade(self, trade):

        self.db.execute(
            """
            INSERT INTO trades
            (
                symbol,
                signal,
                confidence,
                entry,
                stop_loss,
                target1,
                target2,
                quantity,
                risk_reward,
                reasons
            )
            VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                trade.symbol,
                trade.signal,
                trade.confidence,
                trade.entry,
                trade.stop_loss,
                trade.target1,
                trade.target2,
                trade.quantity,
                trade.risk_reward,
                ", ".join(trade.reasons)
            )
        )

    def all(self):

        return self.db.fetchall(
            "SELECT * FROM trades ORDER BY id DESC"
        )
