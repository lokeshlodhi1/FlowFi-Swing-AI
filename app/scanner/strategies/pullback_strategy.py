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

        confidence = 0

        # --------------------------------------------------
        # Trend Validation
        # --------------------------------------------------

        trend_ok = ema20 > ema50 > ema200

        if not trend_ok:
            return self._invalid("EMA Trend Failed")

        confidence += 20

        # --------------------------------------------------
        # Pullback Validation
        # --------------------------------------------------

        if close >= ema20:
            confidence += 15

        elif close >= ema50:
            confidence += 25

        else:
            return self._invalid("Pullback Too Deep")

        # --------------------------------------------------
        # Bullish Candle Validation
        # --------------------------------------------------

        candle_range = high - low

        if candle_range > 0:

            body = abs(close - open_price)

            body_percent = (body / candle_range) * 100

            if close > open_price:

                if body_percent >= 70:
                    confidence += 20

                elif body_percent >= 50:
                    confidence += 15

                else:
                    confidence += 5

        # --------------------------------------------------
        # Volume Validation
        # --------------------------------------------------

        avg_volume = df["Volume"].tail(20).mean()

        current_volume = float(last["Volume"])

        if current_volume >= avg_volume * 2:
            confidence += 20

        elif current_volume >= avg_volume * 1.5:
            confidence += 15

        elif current_volume >= avg_volume:
            confidence += 10

        # --------------------------------------------------
        # Trend Strength
        # --------------------------------------------------

        if close > ema20 > ema50 > ema200:
            confidence += 15

        # --------------------------------------------------
        # Entry
        # --------------------------------------------------

        entry = high

        stop_loss = min(low, ema50)

        risk = entry - stop_loss

        if risk <= 0:
            return self._invalid("Invalid Stop Loss")

        target1 = entry + (risk * 2)
        target2 = entry + (risk * 3)

        rr = round((target1 - entry) / risk, 2)

        # --------------------------------------------------
        # Final Decision
        # --------------------------------------------------

        if confidence >= 90:
            signal = "STRONG BUY"

        elif confidence >= 80:
            signal = "BUY"

        elif confidence >= 65:
            signal = "WATCH"

        else:
            return self._invalid("Confidence Too Low")

        return StrategyResult(
            valid=True,
            setup="PULLBACK",
            confidence=confidence,
            entry=round(entry, 2),
            stop_loss=round(stop_loss, 2),
            target1=round(target1, 2),
            target2=round(target2, 2),
            risk_reward=rr,
            reason=signal,
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