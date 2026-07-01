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

    def scan(self, symbol: str, market_status="BULLISH"):

        # Download market data
        market = self.market_service.get_daily(symbol)

        df = market.data.copy()

        # Fix latest yfinance MultiIndex columns
        if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
            df.columns = df.columns.get_level_values(0)

        # Indicators
        df["EMA20"] = IndicatorEngine.ema(df, 20)
        df["EMA50"] = IndicatorEngine.ema(df, 50)
        df["EMA200"] = IndicatorEngine.ema(df, 200)
        df["AVG_VOLUME"] = IndicatorEngine.average_volume(df)
        df["ATR"] = IndicatorEngine.atr(df)

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
        atr = float(last["ATR"])

        # Generate Signal
        result = self.signal_generator.generate(
            close=close,
            ema20=ema20,
            ema50=ema50,
            ema200=ema200,
            current_volume=volume,
            avg_volume=avg_volume
        )

        # Market Trend Filter
        if market_status == "BEARISH":
            if result["signal"] == "BUY":
                result["signal"] = "WATCH"
                result["confidence"] = max(
                    0,
                    result["confidence"] - 20
                )

        print("\n" + "=" * 60)
        print(symbol)
        print("=" * 60)
        print(result)

        # Ignore weak signals
        if result["signal"] == "IGNORE":
            return None

        # -------------------------------------------------
        # Professional Swing Stop Loss
        # -------------------------------------------------

        swing_low = float(df["Low"].tail(10).min())

        atr_stop = close - (1.5 * atr)

        # Choose safer stop
        stop = min(swing_low, atr_stop)

        # Don't allow stop more than 8% away
        if ((close - stop) / close) > 0.08:
            stop = close * 0.92

        # Reject trades with stop closer than 2%
        risk_percent = ((close - stop) / close) * 100

        if risk_percent < 2:
            print("Rejected : Stop Loss too tight for swing trade")
            return None

        # -------------------------------------------------

        # Position Sizing
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

        reasons.append("ATR Stop Loss")

        trade = TradeBuilder().build(
            symbol=symbol,
            confidence=result["confidence"],
            entry=close,
            stop=stop,
            quantity=risk.quantity,
            reasons=reasons
        )

        trade.signal = result["signal"]

        return trade
