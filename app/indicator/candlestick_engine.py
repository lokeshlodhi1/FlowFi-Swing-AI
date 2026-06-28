import pandas as pd


class CandlestickEngine:

    def __init__(self, df):

        self.df = df.copy()

    def bullish_engulfing(self):

        prev = self.df.shift(1)

        condition = (

            (prev["Close"] < prev["Open"])

            &

            (self.df["Close"] > self.df["Open"])

            &

            (self.df["Open"] < prev["Close"])

            &

            (self.df["Close"] > prev["Open"])

        )

        self.df["Bullish_Engulfing"] = condition

    def bearish_engulfing(self):

        prev = self.df.shift(1)

        condition = (

            (prev["Close"] > prev["Open"])

            &

            (self.df["Close"] < self.df["Open"])

            &

            (self.df["Open"] > prev["Close"])

            &

            (self.df["Close"] < prev["Open"])

        )

        self.df["Bearish_Engulfing"] = condition

    def hammer(self):

        body = abs(self.df["Close"] - self.df["Open"])

        lower = self.df[["Open", "Close"]].min(axis=1) - self.df["Low"]

        upper = self.df["High"] - self.df[["Open", "Close"]].max(axis=1)

        self.df["Hammer"] = (

            (lower > body * 2)

            &

            (upper < body)

        )

    def doji(self):

        body = abs(

            self.df["Close"] -

            self.df["Open"]

        )

        rng = self.df["High"] - self.df["Low"]

        self.df["Doji"] = (

            body

            <=

            rng * 0.1

        )

    def marubozu(self):

        body = abs(

            self.df["Close"]

            -

            self.df["Open"]

        )

        rng = self.df["High"] - self.df["Low"]

        self.df["Marubozu"] = (

            body

            >=

            rng * 0.9

        )

    def calculate(self):

        self.bullish_engulfing()

        self.bearish_engulfing()

        self.hammer()

        self.doji()

        self.marubozu()

        return self.df
