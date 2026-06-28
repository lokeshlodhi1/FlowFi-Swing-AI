import pandas as pd
import ta


class IndicatorEngine:

    def __init__(self, df):

        self.df = df.copy()

    # EMA
    def add_ema(self):

        self.df["EMA20"] = ta.trend.ema_indicator(
            self.df["Close"], window=20
        )

        self.df["EMA50"] = ta.trend.ema_indicator(
            self.df["Close"], window=50
        )

        self.df["EMA200"] = ta.trend.ema_indicator(
            self.df["Close"], window=200
        )

    # ATR
    def add_atr(self):

        self.df["ATR"] = ta.volatility.average_true_range(
            self.df["High"],
            self.df["Low"],
            self.df["Close"]
        )

    # RSI
    def add_rsi(self):

        self.df["RSI"] = ta.momentum.rsi(
            self.df["Close"]
        )

    # MACD
    def add_macd(self):

        macd = ta.trend.MACD(
            self.df["Close"]
        )

        self.df["MACD"] = macd.macd()

        self.df["MACD_SIGNAL"] = macd.macd_signal()

    # Volume

    def add_volume(self):

        self.df["AVG_VOLUME"] = (

            self.df["Volume"]

            .rolling(20)

            .mean()

        )

        self.df["REL_VOLUME"] = (

            self.df["Volume"]

            /

            self.df["AVG_VOLUME"]

        )

    # Calculate everything

    def calculate(self):

        self.add_ema()

        self.add_atr()

        self.add_rsi()

        self.add_macd()

        self.add_volume()

        return self.df
