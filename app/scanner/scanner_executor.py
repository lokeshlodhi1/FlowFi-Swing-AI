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

        market = self.market_service.get_daily(symbol)

        df = market.data.copy()

        # Fix for latest yfinance MultiIndex columns
        if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
            df.columns = df.columns.get_level_values(0)

        # Indicators
        df["EMA20"] = IndicatorEngine.ema(df, 20)
        df["EMA50"] = IndicatorEngine.ema(df, 50)
        df["EMA200"] = IndicatorEngine.ema(df, 200)
        df["AVG_VOLUME"] = IndicatorEngine.average_volume(df)

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

        result = self.signal_generator.generate(
            close=close,
            ema20=ema20,
            ema50=ema50,
            ema200=ema200,
            current_volume=volume,
            avg_volume=avg_volume
        )

        print("\n" + "=" * 60)
        print(symbol)
        print("=" * 60)
        print(result)

        # Ignore weak signals
        if result["signal"] == "IGNORE":
            return None

        # Stop Loss
        if ema20 < close:
            stop = ema20
        else:
            stop = close * 0.98

        risk = self.risk_engine.calculate(
            entry=close,
            stop_loss=stop
        )

        reasons = []

        if result["market"]:
            reasons.append("Market Trend")

        if result["trend"]:
            reasons.append("Strong Trend")

        if result["ema"]:
            reasons.append("EMA Pullback")

        if result["volume"]:
            reasons.append("High Volume")

        trade = TradeBuilder().build(
            symbol=symbol,
            confidence=result["confidence"],
            entry=close,
            stop=stop,
            quantity=risk.quantity,
            reasons=reasons
        )

        # Override signal with calculated decision
        trade.signal = result["signal"]

        return trade
