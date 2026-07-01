from dataclasses import dataclass


@dataclass
class RelativeStrengthResult:
    stock_return: float
    market_return: float
    relative_strength: float
    rating: str
    score: int


class RelativeStrength:

    def __init__(self, stock_close, market_close):
        """
        stock_close : list of stock closing prices
        market_close : list of NIFTY closing prices

        Both lists should have same length.
        """

        self.stock = stock_close
        self.market = market_close

    def calculate(self):

        stock_return = (
            (self.stock[-1] - self.stock[0])
            / self.stock[0]
        ) * 100

        market_return = (
            (self.market[-1] - self.market[0])
            / self.market[0]
        ) * 100

        rs = stock_return - market_return

        if rs >= 10:
            rating = "LEADER"
            score = 100

        elif rs >= 7:
            rating = "VERY_STRONG"
            score = 90

        elif rs >= 5:
            rating = "STRONG"
            score = 80

        elif rs >= 2:
            rating = "GOOD"
            score = 70

        elif rs >= 0:
            rating = "AVERAGE"
            score = 55

        else:
            rating = "WEAK"
            score = 25

        return RelativeStrengthResult(
            stock_return=round(stock_return, 2),
            market_return=round(market_return, 2),
            relative_strength=round(rs, 2),
            rating=rating,
            score=score,
        )