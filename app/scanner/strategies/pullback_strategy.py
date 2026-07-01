from .base_strategy import BaseStrategy, StrategyResult


class PullbackStrategy(BaseStrategy):

    def scan(self):

        df = self.df.copy()

        if len(df) < 60:
            return StrategyResult(
                valid=False,
                setup="PULLBACK",
                confidence=0,
                entry=0,
                stop_loss=0,
                target1=0,
                target2=0,
                risk_reward=0,
                reason="Insufficient Data",
            )

        last = df.iloc[-1]

        close = float(last["Close"])
        high = float(last["High"])
        low = float(last["Low"])

        ema20 = float(last["EMA20"])
        ema50 = float(last["EMA50"])
        ema200 = float(last["EMA200"])

        # --------------------------------------------------
        # Trend Filter
        # --------------------------------------------------

        if not (ema20 > ema50 > ema200):
            return StrategyResult(
                False,
                "PULLBACK",
                0,
                0,
                0,
                0,
                0,
                0,
                "EMA Alignment Failed",
            )

        confidence = 20

        # --------------------------------------------------
        # Pullback Zone
        # --------------------------------------------------

        if close > ema20:
            confidence += 15

        elif close > ema50:
            confidence += 25

        else:
            return StrategyResult(
                False,
                "PULLBACK",
                confidence,
                0,
                0,
                0,
                0,
                0,
                "Price Below EMA50",
            )

        # --------------------------------------------------
        # Bullish Candle
        # --------------------------------------------------

        candle_range = high - low

        if candle_range > 0:

            body = abs(close - float(last["Open"]))

            body_percent = (body / candle_range) * 100

            if body_percent > 60:
                confidence += 15

        # --------------------------------------------------
        # Volume Confirmation
        # --------------------------------------------------

        avg_volume = df["Volume"].tail(20).mean()

        if float(last["Volume"]) > avg_volume * 1.5:
            confidence += 20

        # --------------------------------------------------
        # Trend Strength
        # --------------------------------------------------

        if close > ema20 > ema50 > ema200:
            confidence += 15

        # --------------------------------------------------
        # Entry
        # --------------------------------------------------

        entry = high

        stop = min(low, ema50)

        risk = entry - stop

        if risk <= 0:

            return StrategyResult(
                False,
                "PULLBACK",
                confidence,
                0,
                0,
                0,
                0,
                0,
                "Invalid Risk",
            )

        target1 = entry + (risk * 2)

        target2 = entry + (risk * 3)

        rr = round((target1 - entry) / risk, 2)

        if confidence >= 80:

            return StrategyResult(
                True,
                "PULLBACK",
                confidence,
                round(entry, 2),
                round(stop, 2),
                round(target1, 2),
                round(target2, 2),
                rr,
                "Valid Pullback",
            )

        return StrategyResult(
            False,
            "PULLBACK",
            confidence,
            0,
            0,
            0,
            0,
            0,
            "Confidence Too Low",
        )