from dataclasses import dataclass


@dataclass
class EntryResult:

    setup: str

    signal: str

    confidence: int

    stop_loss: float

    target1: float

    target2: float

    risk_reward: float

    reason: str


class EntryEngine:

    def __init__(self, dataframe):

        self.df = dataframe.copy()

    def analyse(self):

        last = self.df.iloc[-1]

        close = float(last["Close"])

        ema20 = float(last["EMA20"])

        ema50 = float(last["EMA50"])

        high20 = self.df["High"].tail(20).max()

        low20 = self.df["Low"].tail(20).min()

        # --------------------------------------------------
        # Pullback Strategy
        # --------------------------------------------------

        if close > ema20 > ema50:

            stop = low20

            target1 = close + ((close - stop) * 2)

            target2 = close + ((close - stop) * 3)

            return EntryResult(

                setup="PULLBACK",

                signal="BUY",

                confidence=80,

                stop_loss=round(stop,2),

                target1=round(target1,2),

                target2=round(target2,2),

                risk_reward=2.0,

                reason="EMA Pullback"

            )

        # --------------------------------------------------
        # Breakout Strategy
        # --------------------------------------------------

        resistance = self.df["High"].tail(20).max()

        if close > resistance:

            stop = ema20

            target1 = close + ((close-stop)*2)

            target2 = close + ((close-stop)*3)

            return EntryResult(

                setup="BREAKOUT",

                signal="BUY",

                confidence=85,

                stop_loss=round(stop,2),

                target1=round(target1,2),

                target2=round(target2,2),

                risk_reward=2.0,

                reason="20 Day Breakout"

            )

        return EntryResult(

            setup="NONE",

            signal="WATCH",

            confidence=40,

            stop_loss=0,

            target1=0,

            target2=0,

            risk_reward=0,

            reason="No Valid Setup"

        )