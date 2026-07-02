import logging
from datetime import datetime
import numpy as np
import pandas as pd
import yfinance as yf
from app.config.trading_config import *

# Engine imports from your local app package
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
        self.portfolio = PortfolioManager(capital=1000000)
        
        self.capital = INITIAL_CAPITAL
        self.risk_percent = RISK_PERCENT
        self.max_signals = MAX_SIGNALS

    # -------------------------------------------------------------------------
    # Data & Dataframe Preparation
    # -------------------------------------------------------------------------
    def download_data(self, symbol, period="6mo", interval="1d"):
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
            self.logger.error(f"{symbol}: {e}")
            return None

    def prepare_dataframe(self, df):
        df = df.copy()
        df["EMA_FAST"] = self.indicators.ema(df, 20)
        df["EMA_MEDIUM"] = self.indicators.ema(df, 50)
        df["EMA_SLOW"] = self.indicators.ema(df, 200)
        df["RSI"] = self.indicators.rsi(df)
        df["ATR"] = self.indicators.atr(df)
        df["RVOL"] = self.indicators.relative_volume(df)
        return df

    # -------------------------------------------------------------------------
    # Core Market & Stock Scanning Logic
    # -------------------------------------------------------------------------
    def scan_stock(self, symbol):
        try:
            # Download Data
            df = self.download_data(symbol)
            if df is None:
                return None

            # Prepare Indicators
            df = self.prepare_dataframe(df)
            latest = df.iloc[-1]

            # Market Trend Filter
            market = self.market.analyse_market()
            if not market["buy_allowed"]:
                return {
                    "symbol": symbol,
                    "signal": "REJECT",
                    "reason": "Market Filter Failed"
                }

            # Stock Fundamental/Technical Filter
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

            # Entry Strategy Evaluation
            entry = EntryEngine(df).analyse()
            if entry["signal"] == "WATCH":
                return {
                    "symbol": symbol,
                    "signal": "WATCH",
                    "reason": "No Valid Strategy"
                }

            # Risk Assessment & Position Sizing (FIXED: Only passing 2 parameters)
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
                    "reason": risk.reason
                }

            # AI Scoring & Verification
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

            # Rank the accepted setup
            self.signal_ranker.add_signal(
                symbol=symbol,
                market_score=90,
                stock_score=stock_filter.score,
                strategy_score=entry["confidence"],
                confidence=ai.confidence,
                strategy=entry["strategy"],
            )

            # Return Compiled Trade Details
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
            self.logger.exception(f"Scanner Error ({symbol}) : {e}")
            return None

    def scan_market(self, symbols):
        results = []
        self.logger.info(f"Starting scan for {len(symbols)} stocks...")

        for symbol in symbols:
            result = self.scan_stock(symbol)
            if result is None:
                continue

            if result["signal"] in ["BUY", "STRONG BUY"]:
                results.append(result)

        # Process and sort top signals
        ranked = self.signal_ranker.get_top_signals(self.max_signals)
        final_results = []
        for signal in ranked:
            for result in results:
                if result["symbol"] == signal.symbol:
                    result["rank_score"] = signal.score
                    result["recommendation"] = signal.recommendation
                    final_results.append(result)
                    break

        final_results.sort(key=lambda x: x["rank_score"], reverse=True)
        self.logger.info(f"{len(final_results)} BUY signals found.")
        return final_results

    def get_top_signal(self, symbols):
        signals = self.scan_market(symbols)
        if len(signals) == 0:
            return None
        return signals[0]

    # -------------------------------------------------------------------------
    # Execution & Reporting Utilities
    # -------------------------------------------------------------------------
    def run(self, symbols):
        signals = self.scan_market(symbols)
        self.print_summary(signals)
        self.export_signals(signals)
        return signals

    def print_summary(self, signals):
        print("\n" + "=" * 70)
        print("AI SWING TRADING SCANNER")
        print("=" * 70 + "\n")
        for signal in signals:
            print(
                f"{signal['symbol']} | "
                f"{signal['recommendation']} | "
                f"{signal['strategy']} | "
                f"Confidence {signal['confidence']}%"
            )
        print("\n" + "=" * 70)

    def export_signals(self, signals, filename=None):
        if filename is None:
            filename = f"signals_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        if len(signals) == 0:
            self.logger.warning("No signals available.")
            return

        df = pd.DataFrame(signals)
        df.to_csv(filename, index=False)
        self.logger.info(f"Signals exported to {filename}")

    def statistics(self, signals):
        stats = {"total": len(signals), "strong_buy": 0, "buy": 0, "watch": 0}
        for signal in signals:
            if signal["signal"] == "STRONG BUY":
                stats["strong_buy"] += 1
            elif signal["signal"] == "BUY":
                stats["buy"] += 1
            else:
                stats["watch"] += 1
        return stats

    # -------------------------------------------------------------------------
    # Technical Support & Resistance Math
    # -------------------------------------------------------------------------
    def find_swing_high(self, df, LOOKBACK_SWING):
        if len(df) < lookback:
            return None
        return float(df["High"].tail(lookback).max())

    def find_swing_low(self, df, LOOKBACK_SWING):
        if len(df) < lookback:
            return None
        return float(df["Low"].tail(lookback).min())

    def calculate_pullback_percentage(self, current_price, swing_high):
        if swing_high is None:
            return 0
        return round(((swing_high - current_price) / swing_high) * 100, 2)

    def is_healthy_pullback(self, current_price, swing_high):
        pullback = self.calculate_pullback_percentage(current_price, swing_high)
        if 3 <= pullback <= 12:
            return True, pullback
        return False, pullback

    def calculate_atr_percent(self, atr, close):
        if close == 0:
            return 0
        return round((atr / close) * 100, 2)

    def find_resistance(self, df, LOOKBACK_SR):
        if len(df) < lookback:
            return None
        return round(float(df["High"].tail(lookback).max()), 2)

    def find_support(self, df, LOOKBACK_SR):
        if len(df) < lookback:
            return None
        return round(float(df["Low"].tail(lookback).min()), 2)

    def resistance_distance(self, close, resistance):
        if resistance is None:
            return 999
        return round(((resistance - close) / resistance) * 100, 2)

    def support_distance(self, close, support):
        if support is None:
            return 999
        return round(((close - support) / support) * 100, 2)

    def is_breakout(self, close, resistance, tolerance=0.5):
        if resistance is None:
            return False
        return close >= (resistance * (1 + tolerance / 100))

    def near_support(self, close, support, tolerance=2):
        if support is None:
            return False
        distance = (abs(close - support) / support) * 100
        return distance <= tolerance

    # -------------------------------------------------------------------------
    # Volume Analysis
    # -------------------------------------------------------------------------
    def relative_volume(self, df, period=20):
        if len(df) < period:
            return 1.0
        current_volume = float(df.iloc[-1]["Volume"])
        average_volume = float(df["Volume"].tail(period).mean())
        if average_volume == 0:
            return 1.0
        return round(current_volume / average_volume, 2)

    def volume_dry_up(self, df, period=20):
        if len(df) < period:
            return False
        avg20 = float(df["Volume"].tail(period).mean())
        avg5 = float(df["Volume"].tail(5).mean())
        return avg5 < (avg20 * 0.70)

    def volume_breakout(self, df):
        return self.relative_volume(df) >= RVOL_BREAKOUT

    def volume_score(self, df):
        rvol = self.relative_volume(df)
        if rvol >= 3: return 25
        if rvol >= 2: return 20
        if rvol >= 1.5: return 15
        if rvol >= 1.2: return 10
        return 0

    def accumulation(self, df):
        candle = df.iloc[-1]
        close, open_price, high, low, volume = (
            float(candle["Close"]), float(candle["Open"]), 
            float(candle["High"]), float(candle["Low"]), float(candle["Volume"])
        )
        avg_volume = float(df["Volume"].tail(20).mean())
        if high == low:
            return False
        body_percent = (abs(close - open_price) / (high - low)) * 100
        return close > open_price and body_percent >= 60 and volume >= avg_volume * 1.5

    def distribution(self, df):
        candle = df.iloc[-1]
        close, open_price, high, low, volume = (
            float(candle["Close"]), float(candle["Open"]), 
            float(candle["High"]), float(candle["Low"]), float(candle["Volume"])
        )
        avg_volume = float(df["Volume"].tail(20).mean())
        if high == low:
            return False
        body_percent = (abs(close - open_price) / (high - low)) * 100
        return close < open_price and body_percent >= 60 and volume >= avg_volume * 1.5

    # -------------------------------------------------------------------------
    # Scoring & Decision Systems
    # -------------------------------------------------------------------------
    def trend_strength(self, df):
        # FIXED: Replaced placeholder with real dynamic logic based on EMA stacks
        last = df.iloc[-1]
        ema20 = float(last["EMA20"])
        ema50 = float(last["EMA50"])
        ema200 = float(last["EMA200"])
        
        if ema20 > ema50 > ema200:
            return 25  # Strong Uptrend
        elif ema20 > ema50:
            return 15  # Moderate Uptrend
        return 5       # Weak/No Trend

    def ema_slope(self, series, period=5):
        if len(series) < period + 1:
            return 0
        current = float(series.iloc[-1])
        previous = float(series.iloc[-period])
        if previous == 0:
            return 0
        return round(((current - previous) / previous) * 100, 2)

    def price_position_score(self, df):
        last = df.iloc[-1]
        close = float(last["Close"])
        score = 0
        if close > float(last["EMA20"]): score += 20
        if close > float(last["EMA50"]): score += 30
        if close > float(last["EMA200"]): score += 50
        return score

    def momentum_score(self, df):
        rsi = float(df.iloc[-1]["RSI"])
        if 55 <= rsi <= 68: return 30
        if 50 <= rsi < 55: return 20
        if 68 < rsi <= 75: return 15
        return 0

    def trend_grade(self, df):
        trend = self.trend_strength(df)
        position = self.price_position_score(df)
        momentum = self.momentum_score(df)
        total = trend + position + momentum
        if total >= 130: return "A+", total
        if total >= 110: return "A", total
        if total >= 90: return "B", total
        if total >= 70: return "C", total
        return "D", total

    def risk_reward_score(self, entry, stop_loss, target):
        risk = entry - stop_loss
        reward = target - entry
        if risk <= 0:
            return 0
        rr = reward / risk
        if rr >= 3: return 25
        if rr >= 2.5: return 20
        if rr >= 2: return 15
        if rr >= 1.5: return 10
        return 0

    def pullback_score(self, df):
        swing_high = self.find_swing_high(df)
        close = float(df.iloc[-1]["Close"])
        valid, pullback = self.is_healthy_pullback(close, swing_high)
        if not valid:
            return 0
        if 3 <= pullback <= 6: return 25
        if 6 < pullback <= 8: return 20
        return 15

    def breakout_score(self, df):
        resistance = self.find_resistance(df)
        close = float(df.iloc[-1]["Close"])
        if resistance is None:
            return 0
        if self.is_breakout(close, resistance):
            return 25 if self.volume_breakout(df) else 15
        return 0

    def timeframe_score(self, weekly, daily, h4, h2):
        # FIXED: Handles the boolean confirm() method safely now
        has_confirmation = MultiTimeframe().confirm(weekly, daily, h4, h2)
        return 20 if has_confirmation else 0

    def institutional_score(self, df, entry, stop_loss, target, weekly=True, daily=True, h4=True, h2=True):
        trend = self.trend_strength(df)
        volume = self.volume_score(df)
        breakout = self.breakout_score(df)
        pullback = self.pullback_score(df)
        rr = self.risk_reward_score(entry, stop_loss, target)
        timeframe = self.timeframe_score(weekly, daily, h4, h2)
        
        return min(trend + volume + breakout + pullback + rr + timeframe, 100)

    def final_decision(self, score):
        if score >= 90: return "STRONG BUY"
        if score >= 80: return "BUY"
        if score >= 70: return "WATCH"
        return "REJECT"

    # -------------------------------------------------------------------------
    # Position Management / Exits
    # -------------------------------------------------------------------------
    def trailing_stop_loss(self, current_price, atr, multiplier=ATR_MULTIPLIER):
        return round(current_price - (atr * multiplier), ATR_MULTIPLIER)

    def break_even_stop(self, entry, current_price, stop_loss, target1):
        return entry if current_price >= target1 else stop_loss

    def partial_exit(self, current_price, target1, target2):
        if current_price >= target2: return 100
        if current_price >= target1: return 50
        return 0

    def time_exit(self, holding_days, max_days=20):
        return holding_days >= max_days

    def gap_down_exit(self, previous_close, today_open, threshold=3):
        gap = ((previous_close - today_open) / previous_close) * 100
        return gap >= threshold
