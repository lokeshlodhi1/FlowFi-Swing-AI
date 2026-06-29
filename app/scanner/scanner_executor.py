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

        # -------------------------------
        # FIX FOR NEW YFINANCE VERSIONS
        # -------------------------------
        if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
            df.columns = df.columns.get_level_values(0)

        # Calculate Indicators
        df["EMA20"] = IndicatorEngine.ema(df, 20)
        df["EMA50"] = IndicatorEngine.ema(df, 50)
        df["EMA200"] = IndicatorEngine.ema(df, 200)
        df["AVG_VOLUME"] = IndicatorEngine.average_volume(df)

        # Remove rows with NaN indicators
        df = df.dropna()

        if df.empty:
            return None

        last = df.iloc[-1]

        close = float(last["Close"])
        ema20 = float(last["EMA20"])
        ema50 = float(last["EMA50"])
        ema200 = float(last["EMA200"])
        volume = float(last["Volume"])
        avg_volume = float(last["AVG_VOLUME"])

        # Generate Strategy Signals
        signals = self.signal_generator.generate(
            close=close,
            ema20=ema20,
            ema50=ema50,
            ema200=ema200,
            current_volume=volume,
            avg_volume=avg_volume
        )

        # Ignore stock if strategy fails
        if not all(signals.values()):
            return None

        # Position Sizing
        risk = self.risk_engine.calculate(
            entry=close,
            stop_loss=ema20
        )

        # Build Trade Signal
        trade = TradeBuilder().build(
            symbol=symbol,
            confidence=95,
            entry=close,
            stop=ema20,
            quantity=risk.quantity,
            reasons=[
                "EMA20 Pullback",
                "Trend Strong",
                "High Volume"
            ]
        )

        return trade
