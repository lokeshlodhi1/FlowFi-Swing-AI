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

        try:

            # Download market data
            market = self.market_service.get_daily(symbol)

            df = market.data.copy()

            # Handle MultiIndex returned by newer yfinance versions
            if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
                df.columns = df.columns.get_level_values(0)

            # Calculate indicators
            df["EMA20"] = IndicatorEngine.ema(df, 20)
            df["EMA50"] = IndicatorEngine.ema(df, 50)
            df["EMA200"] = IndicatorEngine.ema(df, 200)
            df["AVG_VOLUME"] = IndicatorEngine.average_volume(df)

            df = df.dropna()

            if df.empty:
                print(f"{symbol}: No indicator data")
                return None

            last = df.iloc[-1]

            close = float(last["Close"])
            ema20 = float(last["EMA20"])
            ema50 = float(last["EMA50"])
            ema200 = float(last["EMA200"])
            volume = float(last["Volume"])
            avg_volume = float(last["AVG_VOLUME"])

            signals = self.signal_generator.generate(
                close=close,
                ema20=ema20,
                ema50=ema50,
                ema200=ema200,
                current_volume=volume,
                avg_volume=avg_volume
            )

            print(f"\n========== {symbol} ==========")
            print(signals)

            risk = self.risk_engine.calculate(
                entry=close,
                stop_loss=ema20
            )

            confidence = sum(1 for value in signals.values() if value) * 25

            reasons = []

            if signals.get("market"):
                reasons.append("Market OK")

            if signals.get("trend"):
                reasons.append("Trend Strong")

            if signals.get("ema"):
                reasons.append("EMA Pullback")

            if signals.get("volume"):
                reasons.append("High Volume")

            trade = TradeBuilder().build(
                symbol=symbol,
                confidence=confidence,
                entry=close,
                stop=ema20,
                quantity=risk.quantity,
                reasons=reasons
            )

            return trade

        except Exception as e:
            print(f"{symbol}: {e}")
            return None
