import pandas as pd


class AdvancedIndicator:

    @staticmethod
    def rsi(df, period=14):

        delta = df["Close"].diff()

        gain = delta.clip(lower=0).rolling(period).mean()

        loss = (-delta.clip(upper=0)).rolling(period).mean()

        rs = gain / loss

        return 100 - (100 / (1 + rs))

    @staticmethod
    def macd(df):

        ema12 = df["Close"].ewm(span=12).mean()

        ema26 = df["Close"].ewm(span=26).mean()

        macd = ema12 - ema26

        signal = macd.ewm(span=9).mean()

        return macd, signal

    @staticmethod
    def vwap(df):

        return ((df.High + df.Low + df.Close) / 3 * df.Volume).cumsum() / df.Volume.cumsum()
