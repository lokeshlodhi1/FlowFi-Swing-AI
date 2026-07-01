from dataclasses import dataclass


@dataclass
class RankedSignal:

    symbol: str
    score: float
    confidence: int
    strategy: str
    recommendation: str


class SignalRanker:

    def __init__(self):

        self.signals = []

    def add_signal(

        self,

        symbol,

        market_score,

        stock_score,

        strategy_score,

        confidence,

        strategy,

    ):

        final_score = (

            market_score * 0.25 +

            stock_score * 0.30 +

            strategy_score * 0.30 +

            confidence * 0.15

        )

        if final_score >= 90:

            recommendation = "STRONG BUY"

        elif final_score >= 80:

            recommendation = "BUY"

        elif final_score >= 70:

            recommendation = "WATCH"

        else:

            recommendation = "REJECT"

        self.signals.append(

            RankedSignal(

                symbol=symbol,

                score=round(final_score, 2),

                confidence=confidence,

                strategy=strategy,

                recommendation=recommendation,

            )

        )

    def get_top_signals(

        self,

        limit=10,

    ):

        self.signals.sort(

            key=lambda x: x.score,

            reverse=True,

        )

        return self.signals[:limit]