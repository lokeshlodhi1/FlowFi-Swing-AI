from app.market_data.yahoo_provider import YahooFinanceProvider
from app.market_data.market_data_service import MarketDataService

from app.scanner.indicator_engine import IndicatorEngine
from app.scanner.signal_generator import SignalGenerator

from app.trade.trade_builder import TradeBuilder
from app.risk.risk_engine import RiskEngine


class ScannerExecutor:

    def __init__(self):
        provider = YahooFinanceProvider()
        self.market_service = MarketDataService(provider)
        self.signal_generator = SignalGenerator()
        self.risk_engine = RiskEngine(
            capital=100000,
            risk_percent=1
        )

    def scan(self, symbol: str):

        # Download market data
        market = self.market_service.get_daily(symbol)
        df = market.data.copy()

        # Calculate indicators
        df["EMA20"] = IndicatorEngine.ema(df, 20)
        df["EMA50"] = IndicatorEngine.ema(df, 50)
        df["EMA200"] = IndicatorEngine.ema(df, 200)
        df["AVG_VOLUME"] = IndicatorEngine.average_volume(df)

        last = df.iloc[-1]

        # Generate strategy signals
        signals = self.signal_generator.generate(
            close=float(last["Close"]),
            ema20=float(last["EMA20"]),
            ema50=float(last["EMA50"]),
            ema200=float(last["EMA200"]),
            current_volume=float(last["Volume"]),
            avg_volume=float(last["AVG_VOLUME"])
        )

        # If any required condition fails, ignore the stock
        if not all(signals.values()):
            return None

        entry = float(last["Close"])
        stop = float(last["EMA20"])

        risk = self.risk_engine.calculate(
            entry=entry,
            stop_loss=stop
        )

        trade = TradeBuilder().build(
            symbol=symbol,
            confidence=95,
            entry=entry,
            stop=stop,
            quantity=risk.quantity,
            reasons=[
                "EMA20 Pullback",
                "Trend Strong",
                "High Volume"
            ]
        )

        return trade
