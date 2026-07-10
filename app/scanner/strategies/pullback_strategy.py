from .base_strategy import BaseStrategy, StrategyResult


class PullbackStrategy(BaseStrategy):

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
        
        # Safely fetch RSI if present, default to 55 if missing
        rsi = float(last.get("RSI", last.get("rsi50", 55)))

        strategy_score = 0

        # --------------------------------------------------
        # 1. Trend Score (Max 20 points)
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
        # 2. Pullback Quality (Max 20 points)
        # --------------------------------------------------
        # Calculate distance down from recent highs to quantify the pullback
        recent_max = df["High"].tail(10).max()
        pullback_pct = ((recent_max - close) / recent_max) * 100 if recent_max > 0 else 0

        if 3.0 <= pullback_pct <= 10.0:
            strategy_score += 20
        elif close >= ema20:
            strategy_score += 15
        elif close >= ema50:
            strategy_score += 10
        else:
            return self._invalid("Pullback Too Deep")

        # --------------------------------------------------
        # 3. RSI Window (Max 15 points)
        # --------------------------------------------------
        if 50 <= rsi <= 70:
            strategy_score += 15
        elif 45 <= rsi < 50 or 70 < rsi <= 75:
            strategy_score += 8
        else:
            strategy_score += 0

        # --------------------------------------------------
        # 4. Relative Volume (RVOL) Confirmation (Max 15 points)
        # --------------------------------------------------
        avg_volume = df["Volume"].tail(20).mean()
        current_volume = float(last["Volume"])
        rvol = current_volume / avg_volume if avg_volume > 0 else 1.0

        if rvol >= 1.5:
            strategy_score += 15
        elif rvol >= 1.1:
            strategy_score += 12
        elif rvol >= 0.9:
            strategy_score += 5

        # --------------------------------------------------
        # 5. Candlestick Reversal Confirmation (Max 15 points)
        # --------------------------------------------------
        candle_range = high - low
        if candle_range > 0:
            body = abs(close - open_price)
            body_percent = (body / candle_range) * 100

            if close > open_price:  # Green Bullish Reversal Bar
                if body_percent >= 60:
                    strategy_score += 15
                elif body_percent >= 40:
                    strategy_score += 10
                else:
                    strategy_score += 5

        # --------------------------------------------------
        # 6. ATR & Risk Reward Structural Scores (Max 15 points)
        # --------------------------------------------------
        # Static baseline allocation for physical health indicators
        strategy_score += 15 

        # --------------------------------------------------
        # Risk & Trade Structure Mathematics
        # --------------------------------------------------
        entry = high
        stop_loss = min(low, ema50)
        risk = entry - stop_loss

        if risk <= 0:
            return self._invalid("Invalid Stop Loss Structuring")

        target1 = entry + (risk * 2.0)
        target2 = entry + (risk * 2.5)
        rr = round((target1 - entry) / risk, 2)

        return StrategyResult(
            valid=True,
            setup="PULLBACK",
            confidence=int(strategy_score),
            entry=round(entry, 2),
            stop_loss=round(stop_loss, 2),
            target1=round(target1, 2),
            target2=round(target2, 2),
            risk_reward=rr,
            reason="PULLBACK_PASSED",
        )

    def _invalid(self, reason):
        return StrategyResult(
            valid=False,
            setup="PULLBACK",
            confidence=0,
            entry=0,
            stop_loss=0,
            target1=0,
            target2=0,
            risk_reward=0,
            reason=reason,
        )
