from app.market_data.yahoo_provider import YahooFinanceProvider
from app.market_data.market_data_service import MarketDataService

from .indicator_engine import IndicatorEngine
from .signal_generator import SignalGenerator


class ScannerExecutor:

    def __init__(self):

        provider = YahooFinanceProvider()

        self.service = MarketDataService(provider)

        self.signal = SignalGenerator()

    def scan(self, symbol):

        market = self.service.get_daily(symbol)

        df = market.data.copy()

        df["EMA20"] = IndicatorEngine.ema(df, 20)

        df["EMA50"] = IndicatorEngine.ema(df, 50)

        df["EMA200"] = IndicatorEngine.ema(df, 200)

        df["AVGVOL"] = IndicatorEngine.average_volume(df)

        last = df.iloc[-1]

        result = self.signal.generate(

            close=last["Close"],

            ema20=last["EMA20"],

            ema50=last["EMA50"],

            ema200=last["EMA200"],

            current_volume=last["Volume"],

            avg_volume=last["AVGVOL"]

        )

        return result
