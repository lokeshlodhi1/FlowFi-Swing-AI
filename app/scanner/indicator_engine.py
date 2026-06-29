import pandas as pd


class IndicatorEngine:

    @staticmethod
    def ema(df: pd.DataFrame, period: int):

        return df["Close"].ewm(span=period, adjust=False).mean()

    @staticmethod
    def sma(df: pd.DataFrame, period: int):

        return df["Close"].rolling(period).mean()

    @staticmethod
    def average_volume(df: pd.DataFrame, period=20):

        return df["Volume"].rolling(period).mean()

    @staticmethod
    def atr(df: pd.DataFrame, period=14):

        high_low = df["High"] - df["Low"]

        high_close = (df["High"] - df["Close"].shift()).abs()

        low_close = (df["Low"] - df["Close"].shift()).abs()

        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)

        return tr.rolling(period).mean()
