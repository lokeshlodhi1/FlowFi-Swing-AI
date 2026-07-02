import logging
from datetime import datetime

import pandas as pd
import yfinance as yf

from app.config.trading_config import *

from app.scanner.indicator_engine import IndicatorEngine
from app.market.market_engine import MarketEngine
from app.scanner.entry_engine import EntryEngine
from app.risk.risk_engine import RiskEngine
from app.scanner.stock_filter import StockFilter
from app.scanner.multi_timeframe import MultiTimeframe
from app.scanner.signal_ranker import SignalRanker
from app.ai.ai_confidence_engine import AIConfidenceEngine
from app.risk.portfolio_manager import PortfolioManager


class ScannerExecutor:

    def __init__(self):

        self.logger = logging.getLogger(__name__)

        self.indicators = IndicatorEngine()
        self.market = MarketEngine()
        self.signal_ranker = SignalRanker()

        self.portfolio = PortfolioManager(
            capital=INITIAL_CAPITAL
        )

        self.capital = INITIAL_CAPITAL
        self.risk_percent = RISK_PERCENT
        self.max_signals = MAX_SIGNALS

    # ----------------------------------------------------------
    # DATA DOWNLOAD
    # ----------------------------------------------------------

    def download_data(
        self,
        symbol,
        period="6mo",
        interval="1d",
    ):

        try:

            df = yf.download(
                symbol,
                period=period,
                interval=interval,
                progress=False,
                auto_adjust=False,
            )

            if df.empty:
                return None

            # Fix Yahoo Finance MultiIndex
            if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
                df.columns = df.columns.get_level_values(0)

            return df

        except Exception as e:

            self.logger.error(f"{symbol}: {e}")

            return None

    # ----------------------------------------------------------
    # PREPARE DATAFRAME
    # ----------------------------------------------------------

    def prepare_dataframe(self, df):

        df = df.copy()

        # Fix MultiIndex if required
        if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
            df.columns = df.columns.get_level_values(0)

        df["EMA20"] = self.indicators.ema(df, 20)
        df["EMA50"] = self.indicators.ema(df, 50)
        df["EMA200"] = self.indicators.ema(df, 200)

        df["RSI"] = self.indicators.rsi(df)
        df["ATR"] = self.indicators.atr(df)
        df["RVOL"] = self.indicators.relative_volume(df)

        df = df.dropna()

        return df
    # ----------------------------------------------------------
    # SCAN SINGLE STOCK
    # ----------------------------------------------------------

    def scan_stock(self, symbol):

        try:

            df = self.download_data(symbol)

            if df is None:
                return None

            df = self.prepare_dataframe(df)

            latest = df.iloc[-1]

            market = self.market.analyse_market()

            if not market["buy_allowed"]:

                return {
                    "symbol": symbol,
                    "signal": "REJECT",
                    "reason": "Market Filter Failed",
                }

            stock_filter = StockFilter(
                price=float(latest["Close"]),
                avg_volume=float(df["Volume"].tail(20).mean()),
                delivery=60,
                market_cap=10000,
                atr_percent=float(latest["ATR"] / latest["Close"] * 100),
                relative_strength=80,
            ).evaluate()

            if not stock_filter.passed:

                return {
                    "symbol": symbol,
                    "signal": "REJECT",
                    "reason": stock_filter.reason,
                }

            entry = EntryEngine(df).analyse()

            if entry["signal"] == "WATCH":

                return {
                    "symbol": symbol,
                    "signal": "WATCH",
                    "reason": "No Valid Strategy",
                }

            risk = RiskEngine(
                self.capital,
                self.risk_percent,
            ).calculate(
                entry["entry"],
                entry["stop_loss"],
            )

            if not risk.valid:

                return {
                    "symbol": symbol,
                    "signal": "REJECT",
                    "reason": risk.reason,
                }

            ai = AIConfidenceEngine(
                market_score=market["market_regime"].score,
                stock_score=stock_filter.score,
                strategy_confidence=entry["confidence"],
                risk_reward=entry["risk_reward"],
                relative_strength=80,
            ).evaluate()

            if not ai.passed:

                return {
                    "symbol": symbol,
                    "signal": "REJECT",
                    "reason": "Low AI Confidence",
                }

            self.signal_ranker.add_signal(
                symbol=symbol,
                market_score=market["market_regime"].score,
                stock_score=stock_filter.score,
                strategy_score=entry["confidence"],
                confidence=ai.confidence,
                strategy=entry["strategy"],
            )

            return {
                "symbol": symbol,
                "signal": ai.recommendation,
                "grade": ai.trade_grade,
                "confidence": ai.confidence,
                "strategy": entry["strategy"],
                "entry": entry["entry"],
                "stop_loss": entry["stop_loss"],
                "target1": entry["target1"],
                "target2": entry["target2"],
                "risk_reward": entry["risk_reward"],
                "quantity": risk.quantity,
                "position_value": risk.position_value,
            }

        except Exception as e:

            self.logger.exception(
                f"Scanner Error ({symbol}) : {e}"
            )

            return None
    # ----------------------------------------------------------
    # SCAN COMPLETE MARKET
    # ----------------------------------------------------------

    def scan_market(self, symbols):

        results = []

        self.signal_ranker.signals = []

        self.logger.info(
            f"Scanning {len(symbols)} stocks..."
        )

        for symbol in symbols:

            trade = self.scan_stock(symbol)

            if trade is None:
                continue

            if trade["signal"] not in [
                "BUY",
                "STRONG BUY",
            ]:
                continue

            results.append(trade)

        ranked = self.signal_ranker.get_top_signals(
            self.max_signals
        )

        final_results = []

        for ranked_signal in ranked:

            for trade in results:

                if trade["symbol"] == ranked_signal.symbol:

                    trade["rank_score"] = ranked_signal.score
                    trade["recommendation"] = ranked_signal.recommendation

                    final_results.append(trade)

                    break

        final_results.sort(

            key=lambda x: x["rank_score"],

            reverse=True,

        )

        self.logger.info(

            f"{len(final_results)} BUY signals found."

        )

        return final_results

    # ----------------------------------------------------------
    # GET TOP SIGNAL
    # ----------------------------------------------------------

    def get_top_signal(self, symbols):

        signals = self.scan_market(symbols)

        if len(signals) == 0:

            return None

        return signals[0]

    # ----------------------------------------------------------
    # RUN SCANNER
    # ----------------------------------------------------------

    def run(self, symbols):

        signals = self.scan_market(symbols)

        self.print_summary(signals)

        self.export_signals(signals)

        return signals

    # ----------------------------------------------------------
    # PRINT SUMMARY
    # ----------------------------------------------------------

    def print_summary(self, signals):

        print()

        print("=" * 70)

        print("FLOWFI AI SWING SCANNER")

        print("=" * 70)

        print()

        for signal in signals:

            print(

                f"{signal['symbol']}"

                f" | "

                f"{signal['recommendation']}"

                f" | "

                f"{signal['strategy']}"

                f" | "

                f"{signal['confidence']}%"

            )

        print()

        print("=" * 70)

    # ----------------------------------------------------------
    # EXPORT CSV
    # ----------------------------------------------------------

    def export_signals(

        self,

        signals,

        filename=None,

    ):

        if filename is None:

            filename = (

                f"signals_"

                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"

                ".csv"

            )

        if len(signals) == 0:

            self.logger.warning(

                "No signals found."

            )

            return

        pd.DataFrame(signals).to_csv(

            filename,

            index=False,

        )

        self.logger.info(

            f"Signals exported to {filename}"

        )

    # ----------------------------------------------------------
    # STATISTICS
    # ----------------------------------------------------------

    def statistics(self, signals):

        stats = {

            "total": len(signals),

            "buy": 0,

            "strong_buy": 0,

            "watch": 0,

        }

        for signal in signals:

            if signal["signal"] == "BUY":

                stats["buy"] += 1

            elif signal["signal"] == "STRONG BUY":

                stats["strong_buy"] += 1

            else:

                stats["watch"] += 1

        return stats
    # ----------------------------------------------------------
    # SUPPORT & RESISTANCE
    # ----------------------------------------------------------

    def find_swing_high(self, df, lookback=LOOKBACK_SWING):

        if len(df) < lookback:
            return None

        return float(
            df["High"].tail(lookback).max()
        )

    def find_swing_low(self, df, lookback=LOOKBACK_SWING):

        if len(df) < lookback:
            return None

        return float(
            df["Low"].tail(lookback).min()
        )

    def calculate_pullback_percentage(
        self,
        current_price,
        swing_high,
    ):

        if swing_high is None:
            return 0

        return round(
            ((swing_high - current_price) / swing_high) * 100,
            2,
        )

    def is_healthy_pullback(
        self,
        current_price,
        swing_high,
    ):

        pullback = self.calculate_pullback_percentage(
            current_price,
            swing_high,
        )

        return (
            PULLBACK_MIN
            <= pullback
            <= PULLBACK_MAX,
            pullback,
        )

    def calculate_atr_percent(
        self,
        atr,
        close,
    ):

        if close == 0:
            return 0

        return round(
            (atr / close) * 100,
            2,
        )

    def find_resistance(
        self,
        df,
        lookback=LOOKBACK_SR,
    ):

        if len(df) < lookback:
            return None

        return round(
            float(df["High"].tail(lookback).max()),
            2,
        )

    def find_support(
        self,
        df,
        lookback=LOOKBACK_SR,
    ):

        if len(df) < lookback:
            return None

        return round(
            float(df["Low"].tail(lookback).min()),
            2,
        )

    def is_breakout(
        self,
        close,
        resistance,
        tolerance=BREAKOUT_TOLERANCE,
    ):

        if resistance is None:
            return False

        return close >= (
            resistance
            * (1 + tolerance / 100)
        )

    def near_support(
        self,
        close,
        support,
        tolerance=SUPPORT_TOLERANCE,
    ):

        if support is None:
            return False

        distance = (
            abs(close - support)
            / support
        ) * 100

        return distance <= tolerance
    # ----------------------------------------------------------
    # VOLUME ANALYSIS
    # ----------------------------------------------------------

    def relative_volume(
        self,
        df,
        period=20,
    ):

        if len(df) < period:
            return 1.0

        current_volume = float(
            df.iloc[-1]["Volume"]
        )

        average_volume = float(
            df["Volume"].tail(period).mean()
        )

        if average_volume == 0:
            return 1.0

        return round(
            current_volume / average_volume,
            2,
        )

    def volume_dry_up(
        self,
        df,
        period=20,
    ):

        if len(df) < period:
            return False

        avg20 = float(
            df["Volume"].tail(period).mean()
        )

        avg5 = float(
            df["Volume"].tail(5).mean()
        )

        return avg5 < (avg20 * 0.70)

    def volume_breakout(
        self,
        df,
    ):

        return (
            self.relative_volume(df)
            >= RVOL_BREAKOUT
        )

    def volume_score(
        self,
        df,
    ):

        rvol = self.relative_volume(df)

        if rvol >= 3:
            return 25

        elif rvol >= 2:
            return 20

        elif rvol >= 1.5:
            return 15

        elif rvol >= 1.2:
            return 10

        return 0

    def accumulation(
        self,
        df,
    ):

        candle = df.iloc[-1]

        close = float(candle["Close"])
        open_price = float(candle["Open"])
        high = float(candle["High"])
        low = float(candle["Low"])
        volume = float(candle["Volume"])

        avg_volume = float(
            df["Volume"].tail(20).mean()
        )

        if high == low:
            return False

        body = abs(
            close - open_price
        )

        candle_range = high - low

        body_percent = (
            body / candle_range
        ) * 100

        return (

            close > open_price

            and

            body_percent >= 60

            and

            volume >= avg_volume * 1.5

        )

    def distribution(
        self,
        df,
    ):

        candle = df.iloc[-1]

        close = float(candle["Close"])
        open_price = float(candle["Open"])
        high = float(candle["High"])
        low = float(candle["Low"])
        volume = float(candle["Volume"])

        avg_volume = float(
            df["Volume"].tail(20).mean()
        )

        if high == low:
            return False

        body = abs(
            close - open_price
        )

        candle_range = high - low

        body_percent = (
            body / candle_range
        ) * 100

        return (

            close < open_price

            and

            body_percent >= 60

            and

            volume >= avg_volume * 1.5

        )
    # ----------------------------------------------------------
    # TREND & SCORING
    # ----------------------------------------------------------

    def trend_strength(self, df):

        last = df.iloc[-1]

        ema20 = float(last["EMA20"])
        ema50 = float(last["EMA50"])
        ema200 = float(last["EMA200"])

        score = 0

        if ema20 > ema50:
            score += 10

        if ema50 > ema200:
            score += 10

        if ema20 > ema200:
            score += 5

        return score

    def price_position_score(self, df):

        last = df.iloc[-1]

        close = float(last["Close"])

        score = 0

        if close > float(last["EMA20"]):
            score += 20

        if close > float(last["EMA50"]):
            score += 30

        if close > float(last["EMA200"]):
            score += 50

        return score

    def momentum_score(self, df):

        rsi = float(df.iloc[-1]["RSI"])

        if 55 <= rsi <= 68:
            return 30

        elif 50 <= rsi < 55:
            return 20

        elif 68 < rsi <= 75:
            return 15

        return 0

    def trend_grade(self, df):

        total = (
            self.trend_strength(df)
            + self.price_position_score(df)
            + self.momentum_score(df)
        )

        if total >= 120:
            return "A+", total

        elif total >= 100:
            return "A", total

        elif total >= 80:
            return "B", total

        elif total >= 60:
            return "C", total

        return "D", total

    def risk_reward_score(
        self,
        entry,
        stop_loss,
        target,
    ):

        risk = entry - stop_loss

        reward = target - entry

        if risk <= 0:
            return 0

        rr = reward / risk

        if rr >= 3:
            return 25

        elif rr >= 2.5:
            return 20

        elif rr >= 2:
            return 15

        elif rr >= 1.5:
            return 10

        return 0

    def institutional_score(
        self,
        df,
        entry,
        stop_loss,
        target,
        weekly=True,
        daily=True,
        h4=True,
        h2=True,
    ):

        timeframe = MultiTimeframe().confirm(
            weekly,
            daily,
            h4,
            h2,
        )

        score = (
            self.trend_strength(df)
            + self.volume_score(df)
            + self.risk_reward_score(
                entry,
                stop_loss,
                target,
            )
        )

        if timeframe:
            score += 20

        return min(score, 100)

    def trailing_stop_loss(
        self,
        current_price,
        atr,
        multiplier=ATR_MULTIPLIER,
    ):

        return round(
            current_price - (atr * multiplier),
            2,
        )

    def break_even_stop(
        self,
        entry,
        current_price,
        stop_loss,
        target1,
    ):

        if current_price >= target1:
            return entry

        return stop_loss

    def partial_exit(
        self,
        current_price,
        target1,
        target2,
    ):

        if current_price >= target2:
            return 100

        elif current_price >= target1:
            return 50

        return 0

    def time_exit(
        self,
        holding_days,
        max_days=20,
    ):

        return holding_days >= max_days

    def gap_down_exit(
        self,
        previous_close,
        today_open,
        threshold=3,
    ):

        gap = (
            (previous_close - today_open)
            / previous_close
        ) * 100

        return gap >= threshold