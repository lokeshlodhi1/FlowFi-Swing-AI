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

        confidence = 0

        # -------------------------------------------------
        # Trend
        # -------------------------------------------------

        if not (ema20 > ema50 > ema200):

            return self._invalid("Trend Failed")

        confidence += 20

        # -------------------------------------------------
        # Volatility Contraction
        # -------------------------------------------------

        range1 = (

            df["High"].tail(20).max()

            -

            df["Low"].tail(20).min()

        )

        range2 = (

            df["High"].tail(10).max()

            -

            df["Low"].tail(10).min()

        )

        if range2 >= range1:

            return self._invalid("No Contraction")

        confidence += 20

        # -------------------------------------------------
        # Volume Dry Up
        # -------------------------------------------------

        avg20 = df["Volume"].tail(20).mean()

        avg5 = df["Volume"].tail(5).mean()

        if avg5 < avg20:

            confidence += 20

        else:

            return self._invalid("Volume Not Dry")

        # -------------------------------------------------
        # Pivot
        # -------------------------------------------------

        pivot = df["High"].tail(10).max()

        if close <= pivot:

            return self._invalid("Below Pivot")

        confidence += 20

        # -------------------------------------------------
        # Entry
        # -------------------------------------------------

        entry = close

        stop = df["Low"].tail(10).min()

        risk = entry - stop

        if risk <= 0:

            return self._invalid("Invalid Risk")

        target1 = entry + (risk * 2)

        target2 = entry + (risk * 3)

        rr = round(

            (target1 - entry)

            /

            risk,

            2

        )

        confidence += 20

        return StrategyResult(

            valid=True,

            setup="VCP",

            confidence=confidence,

            entry=round(entry,2),

            stop_loss=round(stop,2),

            target1=round(target1,2),

            target2=round(target2,2),

            risk_reward=rr,

            reason="Valid VCP"

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

            reason=reason

        )