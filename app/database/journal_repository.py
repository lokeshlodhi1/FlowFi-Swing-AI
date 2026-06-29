from .database import Database


class JournalRepository:

    def __init__(self):

        self.db = Database()

    def add(

        self,

        symbol,

        entry,

        exit_price,

        pnl,

        holding,

        remarks

    ):

        self.db.execute(

            """
            INSERT INTO journal
            (
                symbol,
                entry,
                exit,
                pnl,
                holding_days,
                remarks
            )
            VALUES
            (?, ?, ?, ?, ?, ?)
            """,

            (

                symbol,

                entry,

                exit_price,

                pnl,

                holding,

                remarks

            )

        )

    def all(self):

        return self.db.fetchall(

            "SELECT * FROM journal ORDER BY id DESC"

        )
