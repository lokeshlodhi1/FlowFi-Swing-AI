from .database import Database


class SignalRepository:

    def __init__(self):

        self.db = Database()

    def add_signal(

        self,

        symbol,

        score,

        signal

    ):

        self.db.execute(

            """
            INSERT INTO signals
            (symbol, score, signal)
            VALUES
            (?, ?, ?)
            """,

            (

                symbol,

                score,

                signal

            )

        )

    def all(self):

        return self.db.fetchall(

            "SELECT * FROM signals ORDER BY id DESC"

        )
