import sqlite3
from pathlib import Path


class Database:

    def __init__(self, db_name="flowfi.db"):

        Path("database").mkdir(exist_ok=True)

        self.connection = sqlite3.connect(
            f"database/{db_name}",
            check_same_thread=False
        )

        self.cursor = self.connection.cursor()

    def execute(self, query, values=()):

        self.cursor.execute(query, values)

        self.connection.commit()

    def fetchall(self, query, values=()):

        self.cursor.execute(query, values)

        return self.cursor.fetchall()

    def fetchone(self, query, values=()):

        self.cursor.execute(query, values)

        return self.cursor.fetchone()

    def close(self):

        self.connection.close()
