from dataclasses import dataclass


@dataclass
class StockQualityResult:

    score: int
    grade: str

    relative_strength: int
    liquidity: int
    volume: int
    volatility: int
    delivery: int
    market_cap: int

    eligible: bool


class StockQuality:

    def __init__(
        self,
        rs_score,
        liquidity_score,
        volume_score,
        atr_score,
        delivery_score,
        market_cap_score,
    ):

        self.rs = rs_score
        self.liquidity = liquidity_score
        self.volume = volume_score
        self.atr = atr_score
        self.delivery = delivery_score
        self.market_cap = market_cap_score

    def evaluate(self):

        total = (
            (self.rs * 0.30)
            + (self.liquidity * 0.20)
            + (self.volume * 0.15)
            + (self.atr * 0.10)
            + (self.delivery * 0.10)
            + (self.market_cap * 0.15)
        )

        total = round(total)

        if total >= 90:
            grade = "A+"

        elif total >= 80:
            grade = "A"

        elif total >= 70:
            grade = "B"

        elif total >= 60:
            grade = "C"

        else:
            grade = "REJECT"

        return StockQualityResult(

            score=total,

            grade=grade,

            relative_strength=self.rs,

            liquidity=self.liquidity,

            volume=self.volume,

            volatility=self.atr,

            delivery=self.delivery,

            market_cap=self.market_cap,

            eligible=total >= 70,
        )