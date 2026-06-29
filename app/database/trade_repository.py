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
                entry,
                stop_loss,
                target1,
                target2,
                quantity,
                confidence,
                risk_reward,
                status
            )
            VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                trade.symbol,
                trade.signal,
                trade.entry,
                trade.stop_loss,
                trade.target1,
                trade.target2,
                trade.quantity,
                trade.confidence,
                trade.risk_reward,
                "OPEN"
            )
        )

    def get_open_trades(self):

        return self.db.fetchall(

            "SELECT * FROM trades WHERE status='OPEN'"

        )

    def close_trade(self, trade_id):

        self.db.execute(

            "UPDATE trades SET status='CLOSED' WHERE id=?",

            (trade_id,)

        )
