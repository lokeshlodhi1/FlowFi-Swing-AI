from dataclasses import dataclass

from app.market_data.yahoo_provider import YahooFinanceProvider
from app.market_data.market_data_service import MarketDataService
from app.scanner.indicator_engine import IndicatorEngine


@dataclass
class MarketTrendResult:
    trend: str
    close: float
    ema20: float
    ema50: float
    ema200: float
    trend_strength: int
    bullish_alignment: bool


class MarketTrend:

    def __init__(self):
        provider = YahooFinanceProvider()
        self.market = MarketDataService(provider)

    def get_trend(self):

        market = self.market.get_daily("^NSEI")

        df = market.data.copy()

        # Fix yfinance MultiIndex
        if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
            df.columns = df.columns.get_level_values(0)

        df["EMA20"] = IndicatorEngine.ema(df, 20)
        df["EMA50"] = IndicatorEngine.ema(df, 50)
        df["EMA200"] = IndicatorEngine.ema(df, 200)

        df = df.dropna()

        last = df.iloc[-1]

        close = float(last["Close"])
        ema20 = float(last["EMA20"])
        ema50 = float(last["EMA50"])
        ema200 = float(last["EMA200"])

        trend_strength = 0

        if close > ema20:
            trend_strength += 25

        if ema20 > ema50:
            trend_strength += 25

        if ema50 > ema200:
            trend_strength += 25

        if close > ema200:
            trend_strength += 25

        bullish_alignment = ema20 > ema50 > ema200
bearish_alignment = ema20 < ema50 < ema200

# Improved trend classification
if bullish_alignment:
    trend = "BULLISH"

elif trend_strength >= 75:
    trend = "BULLISH"

elif trend_strength >= 50:
    trend = "SIDEWAYS"

elif bearish_alignment:
    trend = "BEARISH"

else:
    trend = "SIDEWAYS"

   print(
    f"NIFTY Trend: {trend} | "
    f"Close={close:.2f} | "
    f"EMA20={ema20:.2f} | "
    f"EMA50={ema50:.2f} | "
    f"EMA200={ema200:.2f} | "
    f"Strength={trend_strength}"
)

        return MarketTrendResult(
            trend=trend,
            close=close,
            ema20=ema20,
            ema50=ema50,
            ema200=ema200,
            trend_strength=trend_strength,
            
bullish_alignment=(trend == "BULLISH"),,
        )