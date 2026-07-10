from .base_strategy import BaseStrategy, StrategyResult


class BreakoutStrategy(BaseStrategy):

    def scan(self):
        df = self.df.copy()

        if len(df) < 60:
            return self._invalid("Insufficient Data")

        last = df.iloc[-1]

        close = float(last["Close"])
        open_price = float(last["Open"])
        high = float(last["High"])
        low = float(last["Low"])

        ema20 = float(last["EMA20"])
        ema50 = float(last["EMA50"])
        ema200 = float(last["EMA200"])
        
        rsi = float(last.get("RSI", last.get("rsi50", 60)))

        strategy_score = 0

        # --------------------------------------------------
        # 1. Trend Score Allocation (Max 20 points)
        # --------------------------------------------------
        if ema20 > ema50 > ema200:
            strategy_score += 20  # Perfect Alignment
        elif close > ema20 > ema50:
            strategy_score += 15  # Moderate Alignment
        elif close > ema50:
            strategy_score += 10  # Weak Alignment
        else:
            strategy_score += 0

        # --------------------------------------------------
        # 2. Breakout & Consolidation Quality (Max 25 points)
        # --------------------------------------------------
        # Lookback across structural window (20-60 days consolidation)
        resistance = df["High"].iloc[-30:-1].max()
        breakout_percent = ((close - resistance) / resistance) * 100 if resistance > 0 else 0

        if close > resistance and breakout_percent <= 5.0:
            strategy_score += 25  # Ideal Breakout Zone
        elif close > resistance and breakout_percent <= 7.0:
            strategy_score += 15  # Slightly extended breakout
        else:
            return self._invalid("No Breakout or Over-Extended (>5-7%)")

        # --------------------------------------------------
        # 3. Relative Volume (RVOL) Confirmation (Max 20 points)
        # --------------------------------------------------
        avg_volume = df["Volume"].tail(20).mean()
        current_volume = float(last["Volume"])
        rvol = current_volume / avg_volume if avg_volume > 0 else 1.0

        if rvol >= 2.0:
            strategy_score += 20
        elif rvol >= 1.3:
            strategy_score += 15
        elif rvol >= 1.0:
            strategy_score += 5

        # --------------------------------------------------
        # 4. Candlestick Confirmation (Max 15 points)
        # --------------------------------------------------
        candle_range = high - low
        if candle_range > 0:
            body = abs(close - open_price)
            body_percent = (body / candle_range) * 100

            if close > open_price:  # Strong Marubozu / Bullish expansion candle
                if body_percent >= 70:
                    strategy_score += 15
                elif body_percent >= 50:
                    strategy_score += 10

        # --------------------------------------------------
        # 5. RSI Window (Max 10 points)
        # --------------------------------------------------
        if 55 <= rsi <= 75:
            strategy_score += 10
        elif 50 <= rsi < 55:
            strategy_score += 5

        # --------------------------------------------------
        # 6. ATR Volatility Alignment (Max 10 points)
        # --------------------------------------------------
        strategy_score += 10  # Static baseline allocation for healthy range

        # --------------------------------------------------
        # Risk & Trade Structure Mathematics
        # --------------------------------------------------
        entry = close
        # Set a logical stop loss structurally below the breakout line or moving average
        stop_loss = min(resistance * 0.98, ema20) 
        risk = entry - stop_loss

        if risk <= 0:
            return self._invalid("Invalid Structural Risk Bounds")

        target1 = entry + (risk * 2.0)
        target2 = entry + (risk * 2.5)
        rr = round((target1 - entry) / risk, 2)

        return StrategyResult(
            valid=True,
            setup="BREAKOUT",
            confidence=int(strategy_score),
            entry=round(entry, 2),
            stop_loss=round(stop_loss, 2),
            target1=round(target1, 2),
            target2=round(target2, 2),
            risk_reward=rr,
            reason="BREAKOUT_PASSED",
        )

    def _invalid(self, reason):
        return StrategyResult(
            valid=False,
            setup="BREAKOUT",
            confidence=0,
            entry=0,
            stop_loss=0,
            target1=0,
            target2=0,
            risk_reward=0,
            reason=reason,
        )
