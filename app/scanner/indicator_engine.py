import pandas as pd
import numpy as np


class IndicatorEngine:

    @staticmethod
    def ema(df, period):

        return df["Close"].ewm(
            span=period,
            adjust=False
        ).mean()

    @staticmethod
    def sma(df, period):

        return df["Close"].rolling(period).mean()

    @staticmethod
    def rsi(df, period=14):

        delta = df["Close"].diff()

        gain = delta.where(delta > 0, 0)

        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(period).mean()

        avg_loss = loss.rolling(period).mean()

        rs = avg_gain / avg_loss.replace(0, np.nan)

        rsi = 100 - (100 / (1 + rs))

        return rsi.fillna(50)

    @staticmethod
    def atr(df, period=14):

        high_low = df["High"] - df["Low"]

        high_close = abs(df["High"] - df["Close"].shift())

        low_close = abs(df["Low"] - df["Close"].shift())

        tr = pd.concat(
            [high_low, high_close, low_close],
            axis=1
        ).max(axis=1)

        return tr.rolling(period).mean()

    @staticmethod
    def macd(

        df,

        fast=12,

        slow=26,

        signal=9,

    ):

        ema_fast = df["Close"].ewm(
            span=fast,
            adjust=False
        ).mean()

        ema_slow = df["Close"].ewm(
            span=slow,
            adjust=False
        ).mean()

        macd = ema_fast - ema_slow

        signal_line = macd.ewm(
            span=signal,
            adjust=False
        ).mean()

        histogram = macd - signal_line

        return macd, signal_line, histogram

    @staticmethod
    def relative_volume(df, period=20):

        avg = df["Volume"].rolling(period).mean()

        return df["Volume"] / avg

    @staticmethod
    def adx(df, period=14):

        high = df["High"]

        low = df["Low"]

        close = df["Close"]

        plus_dm = high.diff()

        minus_dm = -low.diff()

        plus_dm[plus_dm < 0] = 0

        minus_dm[minus_dm < 0] = 0

        tr = pd.concat([
            high - low,
            abs(high - close.shift()),
            abs(low - close.shift())
        ], axis=1).max(axis=1)

        atr = tr.rolling(period).mean()

        plus_di = (
            100 *
            (plus_dm.rolling(period).mean() / atr)
        )

        minus_di = (
            100 *
            (minus_dm.rolling(period).mean() / atr)
        )

        dx = (

            abs(

                plus_di - minus_di

            )

            /

            (

                plus_di + minus_di

            )

        ) * 100

        return dx.rolling(period).mean()