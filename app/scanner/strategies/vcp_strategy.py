from .base_strategy import BaseStrategy, StrategyResult


class VCPStrategy(BaseStrategy):

    def scan(self):
        df = self.df.copy()

        if len(df) < 80:
            return self._invalid("Insufficient Data")

        last = df.iloc[-1]

        close = float(last["Close"])
        high = float(last["High"])
        low = float(last["Low"])

        ema20 = float(last["EMA20"])
        ema50 = float(last["EMA50"])
        ema200 = float(last["EMA200"])
        
        rsi = float(last.get("RSI", last.get("rsi50", 65)))

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
        # 2. VCP Pattern Volatility Contraction (Max 25 points)
        # --------------------------------------------------
        range1 = df["High"].iloc[-30:-15].max() - df["Low"].iloc[-30:-15].min()
        range2 = df["High"].iloc[-15:-5].max() - df["Low"].iloc[-15:-5].min()
        range3 = df["High"].iloc[-5:].max() - df["Low"].iloc[-5:].min()

        if range3 < range2 < range1:
            strategy_score += 25  # Perfect 3-contraction progressive tightening
        elif range3 < range2:
            strategy_score += 18  # Strong 2-contraction progressive tightening
        elif range2 < range1:
            strategy_score += 10  # Mild tightening setup
        else:
            strategy_score += 0   # No hard rejection anymore

        # --------------------------------------------------
        # 3. Volume Drying Up (Max 20 points)
        # --------------------------------------------------
        avg20 = df["Volume"].tail(20).mean()
        avg5 = df["Volume"].tail(5).mean()

        if avg5 < (avg20 * 0.8):
            strategy_score += 20  # Ideal volume dry-up
        elif avg5 < avg20:
            strategy_score += 15  # Acceptable volume dry-up
        else:
            strategy_score += 5   # Volume is flat or slightly active

        # --------------------------------------------------
        # 4. Tight Pivot Breakout Validation (Max 15 points)
        # --------------------------------------------------
        # Track the recent structural overhead boundary level
        pivot = df["High"].iloc[-10:-1].max()
        pivot_distance = ((close - pivot) / pivot) * 100 if pivot > 0 else 0

        if close >= pivot and pivot_distance <= 3.0:
            strategy_score += 15  # Breaking out cleanly near pivot
        elif abs(pivot_distance) <= 2.0:
            strategy_score += 10  # Tight consolidation coiled right under pivot
        else:
            strategy_score += 0

        # --------------------------------------------------
        # 5. Relative Strength & RSI Windows (Max 20 points)
        # --------------------------------------------------
        # Scoring high relative strength criteria out of the baseline allocations
        if 55 <= rsi <= 75:
            strategy_score += 20
        elif 50 <= rsi < 55:
            strategy_score += 10

        # --------------------------------------------------
        # Risk & Trade Structure Mathematics
        # --------------------------------------------------
        entry = close
        # Set a logical protective swing stop using recent 10-day structural lows
        stop = df["Low"].tail(10).min()
        risk = entry - stop

        if risk <= 0:
            return self._invalid("Invalid Structural Risk Bounds")

        target1 = entry + (risk * 2.0)
        target2 = entry + (risk * 2.5)
        rr = round((target1 - entry) / risk, 2)

        return StrategyResult(
            valid=True,
            setup="VCP",
            confidence=int(strategy_score),
            entry=round(entry, 2),
            stop_loss=round(stop, 2),
            target1=round(target1, 2),
            target2=round(target2, 2),
            risk_reward=rr,
            reason="VCP_PASSED",
        )

    def _invalid(self, reason):
        return StrategyResult(
            valid=False,
            setup="VCP",
            confidence=0,
            entry=0,
            stop_loss=0,
            target1=0,
            target2=0,
            risk_reward=0,
            reason=reason,
        )
