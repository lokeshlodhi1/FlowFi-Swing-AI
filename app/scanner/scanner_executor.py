import logging
from datetime import datetime

import numpy as np
import pandas as pd
import yfinance as yf

from app.scanner.indicator_engine import IndicatorEngine
from app.market.market_engine import MarketEngine
from app.scanner.entry_engine import EntryEngine
from app.risk.risk_engine import RiskEngine
from app.scanner.stock_filter import StockFilter
from app.scanner.multi_timeframe import MultiTimeframe
from app.scanner.signal_ranker import SignalRanker
from app.ai.ai_confidence_engine import AIConfidenceEngine
from app.risk.portfolio_manager import PortfolioManager

def __init__(self):

    self.logger = logging.getLogger(__name__)

    self.indicators = IndicatorEngine()

    self.market = MarketEngine()

    self.signal_ranker = SignalRanker()

    self.portfolio = PortfolioManager(
        capital=1000000
    )

    self.capital = 1000000

    self.risk_percent = 1.0

    self.max_signals = 10

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

        )

        if df.empty:

            return None

        return df

    except Exception as e:

        self.logger.error(

            f"{symbol}: {e}"

        )

        return None

def prepare_dataframe(

    self,

    df,

):

    df = df.copy()

    df["EMA20"] = self.indicators.ema(df, 20)

    df["EMA50"] = self.indicators.ema(df, 50)

    df["EMA200"] = self.indicators.ema(df, 200)

    df["RSI"] = self.indicators.rsi(df)

    df["ATR"] = self.indicators.atr(df)

    df["RVOL"] = self.indicators.relative_volume(df)

    return df


def scan_stock(

    self,

    symbol,

):

    try:

        # ----------------------------------
        # Download Data
        # ----------------------------------

        df = self.download_data(symbol)

        if df is None:

            return None

        # ----------------------------------
        # Prepare Indicators
        # ----------------------------------

        df = self.prepare_dataframe(df)

        latest = df.iloc[-1]

        # ----------------------------------
        # Market Trend
        # ----------------------------------

        market = self.market.analyse_market()

        if not market["buy_allowed"]:

            return {

                "symbol": symbol,

                "signal": "REJECT",

                "reason": "Market Filter Failed"

            }

        # ----------------------------------
        # Stock Filter
        # ----------------------------------

        stock_filter = StockFilter(

            price=float(latest["Close"]),

            avg_volume=float(df["Volume"].tail(20).mean()),

            delivery=60,

            market_cap=10000,

            atr_percent=(latest["ATR"] / latest["Close"]) * 100,

            relative_strength=80,

        ).evaluate()

        if not stock_filter.passed:

            return {

                "symbol": symbol,

                "signal": "REJECT",

                "reason": stock_filter.reason

            }

        # ----------------------------------
        # Entry Engine
        # ----------------------------------

        entry = EntryEngine(df).analyse()

        if entry["signal"] == "WATCH":

            return {

                "symbol": symbol,

                "signal": "WATCH",

                "reason": "No Valid Strategy"

            }

        # ----------------------------------
        # Risk Engine
        # ----------------------------------

        risk = RiskEngine(

            self.capital,

            self.risk_percent,

        ).calculate(

            entry["entry"],

            entry["stop_loss"],

            entry["target1"],

            entry["target2"],

        )

        if not risk.valid:

            return {

                "symbol": symbol,

                "signal": "REJECT",

                "reason": risk.reason

            }

        # ----------------------------------
        # AI Confidence
        # ----------------------------------

        ai = AIConfidenceEngine(

            market_score=90,

            stock_score=stock_filter.score,

            strategy_confidence=entry["confidence"],

            risk_reward=entry["risk_reward"],

            relative_strength=80,

        ).evaluate()

        if not ai.passed:

            return {

                "symbol": symbol,

                "signal": "REJECT",

                "reason": "Low AI Confidence"

            }

        # ----------------------------------
        # Rank Signal
        # ----------------------------------

        self.signal_ranker.add_signal(

            symbol=symbol,

            market_score=90,

            stock_score=stock_filter.score,

            strategy_score=entry["confidence"],

            confidence=ai.confidence,

            strategy=entry["strategy"],

        )

        # ----------------------------------
        # Final Result
        # ----------------------------------

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

def scan_market(

    self,

    symbols,

):

    results = []

    self.logger.info(

        f"Starting scan for {len(symbols)} stocks..."

    )

    for symbol in symbols:

        result = self.scan_stock(symbol)

        if result is None:

            continue

        if result["signal"] in [

            "BUY",

            "STRONG BUY",

        ]:

            results.append(result)

    # ----------------------------------
    # Rank Signals
    # ----------------------------------

    ranked = self.signal_ranker.get_top_signals(

        self.max_signals

    )

    final_results = []

    for signal in ranked:

        for result in results:

            if result["symbol"] == signal.symbol:

                result["rank_score"] = signal.score

                result["recommendation"] = signal.recommendation

                final_results.append(result)

                break

    final_results.sort(

        key=lambda x: x["rank_score"],

        reverse=True,

    )

    self.logger.info(

        f"{len(final_results)} BUY signals found."

    )

    return final_results

def get_top_signal(

    self,

    symbols,

):

    signals = self.scan_market(

        symbols

    )

    if len(signals) == 0:

        return None

    return signals[0]

def print_summary(

    self,

    signals,

):

    print()

    print("=" * 70)

    print("AI SWING TRADING SCANNER")

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

            f"Confidence "

            f"{signal['confidence']}%"

        )

    print()

    print("=" * 70)

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
                "No signals available."
            )

            return

        df = pd.DataFrame(signals)

        df.to_csv(

            filename,

            index=False,

        )

        self.logger.info(

            f"Signals exported to {filename}"

        )

    def statistics(

        self,

        signals,

    ):

        stats = {

            "total": len(signals),

            "strong_buy": 0,

            "buy": 0,

            "watch": 0,

        }

        for signal in signals:

            if signal["signal"] == "STRONG BUY":

                stats["strong_buy"] += 1

            elif signal["signal"] == "BUY":

                stats["buy"] += 1

            else:

                stats["watch"] += 1

        return stats

    def run(

        self,

        symbols,

    ):

        signals = self.scan_market(symbols)

        self.print_summary(signals)

        self.export_signals(signals)

        return signals

    def find_swing_high(self, df, lookback=20):

        if len(df) < lookback:
            return None

        return float(df["High"].tail(lookback).max())

    def find_swing_low(self, df, lookback=20):

        if len(df) < lookback:
            return None

        return float(df["Low"].tail(lookback).min())

    def calculate_pullback_percentage(

        self,

        current_price,

        swing_high,

    ):

        if swing_high is None:

            return 0

        return round(

            (

                (swing_high - current_price)

                /

                swing_high

            )

            * 100,

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

        if 3 <= pullback <= 8:

            return True, pullback

        elif 8 < pullback <= 12:

            return True, pullback

        return False, pullback

    def calculate_atr_percent(

        self,

        atr,

        close,

    ):

        if close == 0:

            return 0

        return round(

            (

                atr /

                close

            )

            * 100,

            2,

        )

    def find_resistance(

        self,

        df,

        lookback=30,

    ):

        if len(df) < lookback:

            return None

        return round(

            float(

                df["High"].tail(lookback).max()

            ),

            2,

        )

    def find_support(

        self,

        df,

        lookback=30,

    ):

        if len(df) < lookback:

            return None

        return round(

            float(

                df["Low"].tail(lookback).min()

            ),

            2,

        )

    def resistance_distance(

        self,

        close,

        resistance,

    ):

        if resistance is None:

            return 999

        return round(

            (

                (resistance - close)

                /

                resistance

            )

            * 100,

            2,

        )

    def support_distance(

        self,

        close,

        support,

    ):

        if support is None:

            return 999

        return round(

            (

                (close - support)

                /

                support

            )

            * 100,

            2,

        )

    def is_breakout(

        self,

        close,

        resistance,

        tolerance=0.5,

    ):

        if resistance is None:

            return False

        return close >= (

            resistance *

            (

                1 +

                tolerance /

                100

            )

        )

    def near_support(

        self,

        close,

        support,

        tolerance=2,

    ):

        if support is None:

            return False

        distance = (

            abs(close - support)

            /

            support

        ) * 100

        return distance <= tolerance

    def relative_volume(

        self,

        df,

        period=20,

    ):

        if len(df) < period:

            return 1.0

        current_volume = float(df.iloc[-1]["Volume"])

        average_volume = float(

            df["Volume"].tail(period).mean()

        )

        if average_volume == 0:

            return 1.0

        return round(

            current_volume /

            average_volume,

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

        rvol = self.relative_volume(df)

        return rvol >= 1.5
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

        body = abs(close - open_price)

        candle_range = high - low

        body_percent = (

            body /

            candle_range

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

        body = abs(close - open_price)

        candle_range = high - low

        body_percent = (

            body /

            candle_range

        ) * 100

        return (

            close < open_price

            and

            body_percent >= 60

            and

            volume >= avg_volume * 1.5

        )

    def ema_slope(

        self,

        series,

        period=5,

    ):

        if len(series) < period + 1:

            return 0

        current = float(series.iloc[-1])

        previous = float(series.iloc[-period])

        if previous == 0:

            return 0

        return round(

            (

                (current - previous)

                /

                previous

            )

            * 100,

            2,

        )

    def price_position_score(

        self,

        df,

    ):

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

    def momentum_score(

        self,

        df,

    ):

        rsi = float(df.iloc[-1]["RSI"])

        score = 0

        if 55 <= rsi <= 68:

            score = 30

        elif 50 <= rsi < 55:

            score = 20

        elif 68 < rsi <= 75:

            score = 15

        else:

            score = 0

        return score

    def trend_grade(

        self,

        df,

    ):

        trend = self.trend_strength(df)

        position = self.price_position_score(df)

        momentum = self.momentum_score(df)

        total = trend + position + momentum

        if total >= 130:

            return "A+", total

        elif total >= 110:

            return "A", total

        elif total >= 90:

            return "B", total

        elif total >= 70:

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
    def pullback_score(

        self,

        df,

    ):

        swing_high = self.find_swing_high(df)

        close = float(df.iloc[-1]["Close"])

        valid, pullback = self.is_healthy_pullback(

            close,

            swing_high,

        )

        if not valid:

            return 0

        if 3 <= pullback <= 6:

            return 25

        elif 6 < pullback <= 8:

            return 20

        return 15

    def breakout_score(

        self,

        df,

    ):

        resistance = self.find_resistance(df)

        close = float(df.iloc[-1]["Close"])

        if resistance is None:

            return 0

        if self.is_breakout(

            close,

            resistance,

        ):

            if self.volume_breakout(df):

                return 25

            return 15

        return 0

    def timeframe_score(

        self,

        weekly,

        daily,

        h4,

        h2,

    ):

        result = MultiTimeframe().confirm(

            weekly,

            daily,

            h4,

            h2,

        )

        return result.score
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

        trend = self.trend_strength(df)

        volume = self.volume_score(df)

        breakout = self.breakout_score(df)

        pullback = self.pullback_score(df)

        rr = self.risk_reward_score(

            entry,

            stop_loss,

            target,

        )

        timeframe = self.timeframe_score(

            weekly,

            daily,

            h4,

            h2,

        )

        total = (

            trend

            + volume

            + breakout

            + pullback

            + rr

            + timeframe

        )

        return min(total, 100)
    def final_decision(

        self,

        score,

    ):

        if score >= 90:

            return "STRONG BUY"

        elif score >= 80:

            return "BUY"

        elif score >= 70:

            return "WATCH"

        return "REJECT"
    def trailing_stop_loss(

        self,

        current_price,

        atr,

        multiplier=2,

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

            /

            previous_close

        ) * 100

        return gap >= threshold
    def exit_decision(

        self,

        current_price,

        trailing_stop,

        holding_days,

        previous_close,

        today_open,

    ):

        if current_price <= trailing_stop:

            return "EXIT"

        if self.time_exit(holding_days):

            return "TIME EXIT"

        if self.gap_down_exit(

            previous_close,

            today_open,

        ):

            return "GAP EXIT"

        return "HOLD"
    def bullish_engulfing(

        self,

        df,

    ):

        if len(df) < 2:

            return False

        prev = df.iloc[-2]

        curr = df.iloc[-1]

        return (

            prev["Close"] < prev["Open"]

            and

            curr["Close"] > curr["Open"]

            and

            curr["Open"] < prev["Close"]

            and

            curr["Close"] > prev["Open"]

        )
    def bearish_engulfing(

        self,

        df,

    ):

        if len(df) < 2:

            return False

        prev = df.iloc[-2]

        curr = df.iloc[-1]

        return (

            prev["Close"] > prev["Open"]

            and

            curr["Close"] < curr["Open"]

            and

            curr["Open"] > prev["Close"]

            and

            curr["Close"] < prev["Open"]

        )
    def hammer(

        self,

        df,

    ):

        candle = df.iloc[-1]

        body = abs(

            candle["Close"] -

            candle["Open"]

        )

        lower = min(

            candle["Close"],

            candle["Open"]

        ) - candle["Low"]

        upper = candle["High"] - max(

            candle["Close"],

            candle["Open"]

        )

        return (

            lower > body * 2

            and

            upper < body

        )
    def shooting_star(

        self,

        df,

    ):

        candle = df.iloc[-1]

        body = abs(

            candle["Close"] -

            candle["Open"]

        )

        upper = candle["High"] - max(

            candle["Close"],

            candle["Open"]

        )

        lower = min(

            candle["Close"],

            candle["Open"]

        ) - candle["Low"]

        return (

            upper > body * 2

            and

            lower < body

        )
    def doji(

        self,

        df,

    ):

        candle = df.iloc[-1]

        body = abs(

            candle["Close"] -

            candle["Open"]

        )

        total = candle["High"] - candle["Low"]

        if total == 0:

            return False

        return (

            body /

            total

        ) <= 0.10
    def candlestick_score(

        self,

        df,

    ):

        score = 0

        if self.bullish_engulfing(df):

            score += 25

        if self.hammer(df):

            score += 20

        if self.doji(df):

            score += 10

        if self.bearish_engulfing(df):

            score -= 25

        if self.shooting_star(df):

            score -= 20

        return score
    def institutional_trade_score(

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

        trend = self.trend_strength(df)

        volume = self.volume_score(df)

        candle = self.candlestick_score(df)

        pullback = self.pullback_score(df)

        breakout = self.breakout_score(df)

        rr = self.risk_reward_score(

            entry,

            stop_loss,

            target,

        )

        timeframe = self.timeframe_score(

            weekly,

            daily,

            h4,

            h2,

        )

        total = (

            trend +

            volume +

            candle +

            pullback +

            breakout +

            rr +

            timeframe

        )

        return min(total, 100)
    def trade_grade(

        self,

        score,

    ):

        if score >= 95:

            return "A+"

        elif score >= 90:

            return "A"

        elif score >= 80:

            return "B"

        elif score >= 70:

            return "C"

        return "D"
    def should_trade(

        self,

        score,

    ):

        return score >= 80
    def confidence_level(

        self,

        score,

    ):

        if score >= 95:

            return 99

        elif score >= 90:

            return 95

        elif score >= 85:

            return 90

        elif score >= 80:

            return 85

        elif score >= 75:

            return 80

        return 70
    def ai_verdict(

        self,

        score,

    ):

        if score >= 95:

            return "Institutional Grade Setup"

        elif score >= 90:

            return "High Probability Swing"

        elif score >= 80:

            return "Good Swing Opportunity"

        elif score >= 70:

            return "Watchlist Candidate"

        return "Avoid Trade"
    def volatility_score(

        self,

        atr_percent,

    ):

        if 2 <= atr_percent <= 5:

            return 25

        elif 1.5 <= atr_percent < 2:

            return 20

        elif 5 < atr_percent <= 7:

            return 15

        return 5
    def ema_alignment(

        self,

        df,

    ):

        last = df.iloc[-1]

        ema20 = float(last["EMA20"])

        ema50 = float(last["EMA50"])

        ema200 = float(last["EMA200"])

        return ema20 > ema50 > ema200
    def trend_quality_score(

        self,

        df,

    ):

        score = 0

        if self.ema_alignment(df):

            score += 40

        trend_score = self.trend_strength(df)

        score += min(trend_score, 40)

        score += self.momentum_score(df)

        return min(score, 100)
    def quality_filter(

        self,

        df,

    ):

        trend = self.trend_quality_score(df)

        volume = self.volume_score(df)

        candle = self.candlestick_score(df)

        total = trend + volume + candle

        return {

            "passed": total >= 100,

            "score": total

        }
        # ==========================================
        # Trend Quality
        # ==========================================

        trend_grade, trend_score = self.trend_grade(df)

        quality = self.quality_filter(df)

        if not quality["passed"]:

            return {

                "symbol": symbol,

                "signal": "REJECT",

                "reason": "Poor Trend Quality"

            }

        # ==========================================
        # Swing Analysis
        # ==========================================

        swing_high = self.find_swing_high(df)

        swing_low = self.find_swing_low(df)

        healthy_pullback, pullback_percent = (

            self.is_healthy_pullback(

                float(latest["Close"]),

                swing_high,

            )

        )

        # ==========================================
        # Support Resistance
        # ==========================================

        resistance = self.find_resistance(df)

        support = self.find_support(df)

        breakout = self.is_breakout(

            float(latest["Close"]),

            resistance,

        )

        near_support = self.near_support(

            float(latest["Close"]),

            support,

        )

        # ==========================================
        # Volume
        # ==========================================

        rvol = self.relative_volume(df)

        accumulation = self.accumulation(df)

        distribution = self.distribution(df)

        volume_score = self.volume_score(df)

        # ==========================================
        # Candlestick
        # ==========================================

        candle_score = self.candlestick_score(df)

        institutional_score = self.institutional_trade_score(

            df,

            entry["entry"],

            entry["stop_loss"],

            entry["target1"],

        )

        trade_grade = self.trade_grade(

            institutional_score

        )

        confidence = self.confidence_level(

            institutional_score

        )

        verdict = self.ai_verdict(

            institutional_score

        )
"institutional_score": institutional_score,

"trade_grade": trade_grade,

"trend_grade": trend_grade,

"trend_score": trend_score,

"volume_score": volume_score,

"candlestick_score": candle_score,

"relative_volume": rvol,

"pullback": pullback_percent,

"support": support,

"resistance": resistance,

"breakout": breakout,

"near_support": near_support,

"accumulation": accumulation,

"distribution": distribution,

"ai_verdict": verdict,

def scan_market(

    self,

    symbols,

):

    results = []

    self.signal_ranker.signals = []

    self.logger.info(

        f"Scanning {len(symbols)} symbols..."

    )

    for symbol in symbols:

        try:

            signal = self.scan_stock(symbol)

            if signal is None:

                continue

            if signal["signal"] not in [

                "BUY",

                "STRONG BUY",

            ]:

                continue

            self.signal_ranker.add_signal(

                symbol=signal["symbol"],

                market_score=90,

                stock_score=signal["institutional_score"],

                strategy_score=signal["trend_score"],

                confidence=signal["confidence"],

                strategy=signal["strategy"],

            )

            results.append(signal)

        except Exception as e:

            self.logger.exception(

                f"{symbol}: {e}"

            )

    ranked = self.signal_ranker.get_top_signals(

        self.max_signals

    )

    final_results = []

    for ranked_signal in ranked:

        for signal in results:

            if signal["symbol"] == ranked_signal.symbol:

                signal["rank"] = len(final_results) + 1

                signal["ranking_score"] = ranked_signal.score

                signal["recommendation"] = ranked_signal.recommendation

                final_results.append(signal)

                break

    return final_results
def build_telegram_message(

    self,

    signal,

):

    return f"""
🟢 {signal['signal']}

━━━━━━━━━━━━━━━━━━

📈 Stock : {signal['symbol']}

🎯 Strategy : {signal['strategy']}

⭐ Grade : {signal['trade_grade']}

🔥 Confidence : {signal['confidence']}%

🏆 Institutional Score : {signal['institutional_score']}

━━━━━━━━━━━━━━━━━━

💰 Entry : {signal['entry']}

🛑 Stop Loss : {signal['stop_loss']}

🎯 Target 1 : {signal['target1']}

🚀 Target 2 : {signal['target2']}

⚖ Risk Reward : {signal['risk_reward']}

━━━━━━━━━━━━━━━━━━

📊 Trend : {signal['trend_grade']}

📦 RVOL : {signal['relative_volume']}x

📈 Volume Score : {signal['volume_score']}

📉 Pullback : {signal['pullback']}%

━━━━━━━━━━━━━━━━━━

🤖 AI Verdict

{signal['ai_verdict']}
"""

def build_all_messages(

    self,

    signals,

):

    messages = []

    for signal in signals:

        messages.append(

            self.build_telegram_message(

                signal

            )

        )

    return messages

def run(

    self,

    symbols,

):

    signals = self.scan_market(

        symbols

    )

    self.print_summary(

        signals

    )

    self.export_signals(

        signals

    )

    telegram_messages = self.build_all_messages(

        signals

    )

    return {

        "signals": signals,

        "telegram": telegram_messages,

        "statistics": self.statistics(

            signals

        ),

    }
