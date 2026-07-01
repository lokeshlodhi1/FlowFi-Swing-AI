from dataclasses import dataclass


@dataclass
class StockFilterResult:

    passed: bool

    score: int

    reason: str


class StockFilter:

    def __init__(

        self,

        price,

        avg_volume,

        delivery,

        market_cap,

        atr_percent,

        relative_strength,

    ):

        self.price = price

        self.avg_volume = avg_volume

        self.delivery = delivery

        self.market_cap = market_cap

        self.atr = atr_percent

        self.rs = relative_strength

    def evaluate(self):

        score = 0

        # ------------------------------------
        # Price Filter
        # ------------------------------------

        if self.price < 100:

            return StockFilterResult(

                False,

                0,

                "Price Below ₹100"

            )

        score += 10

        # ------------------------------------
        # Average Volume
        # ------------------------------------

        if self.avg_volume >= 500000:

            score += 20

        elif self.avg_volume >= 250000:

            score += 15

        else:

            return StockFilterResult(

                False,

                score,

                "Low Volume"

            )

        # ------------------------------------
        # Delivery
        # ------------------------------------

        if self.delivery >= 50:

            score += 20

        elif self.delivery >= 40:

            score += 10

        # ------------------------------------
        # Market Cap
        # ------------------------------------

        if self.market_cap >= 10000:

            score += 20

        elif self.market_cap >= 5000:

            score += 15

        else:

            score += 5

        # ------------------------------------
        # ATR
        # ------------------------------------

        if 2 <= self.atr <= 6:

            score += 15

        elif 1 <= self.atr <= 8:

            score += 8

        # ------------------------------------
        # Relative Strength
        # ------------------------------------

        score += int(self.rs * 0.15)

        passed = score >= 70

        return StockFilterResult(

            passed,

            score,

            "PASS" if passed else "REJECT"

        )