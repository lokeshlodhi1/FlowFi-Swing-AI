class CandlestickPatterns:

    @staticmethod
    def bullish_engulfing(df):

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

    @staticmethod
    def hammer(df):

        candle = df.iloc[-1]

        body = abs(candle["Close"] - candle["Open"])

        lower = min(
            candle["Open"],
            candle["Close"]
        ) - candle["Low"]

        upper = candle["High"] - max(
            candle["Open"],
            candle["Close"]
        )

        return (

            lower > body * 2

            and

            upper < body

        )

    @staticmethod
    def bullish_marubozu(df):

        candle = df.iloc[-1]

        rng = candle["High"] - candle["Low"]

        if rng == 0:
            return False

        body = abs(
            candle["Close"] - candle["Open"]
        )

        return (

            body / rng

        ) > 0.90

    @staticmethod
    def morning_star(df):

        if len(df) < 3:
            return False

        c1 = df.iloc[-3]
        c2 = df.iloc[-2]
        c3 = df.iloc[-1]

        return (

            c1["Close"] < c1["Open"]

            and

            abs(c2["Close"] - c2["Open"])

            <

            abs(c1["Close"] - c1["Open"]) * 0.5

            and

            c3["Close"] > c3["Open"]

        )