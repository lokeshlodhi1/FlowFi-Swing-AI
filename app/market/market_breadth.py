from dataclasses import dataclass

import pandas as pd


@dataclass
class MarketBreadthResult:

    total_stocks: int

    advancing: int
    declining: int

    advance_decline_ratio: float

    above_20ema: int
    above_50ema: int
    above_200ema: int

    breadth_score: int

    market_health: str


class MarketBreadth:

    def __init__(self, stocks_data):

        """
        stocks_data = list of dictionaries

        Example:

        [
            {
                "close": 2540,
                "ema20": 2515,
                "ema50": 2470,
                "ema200": 2205
            },
            ...
        ]
        """

        self.stocks = stocks_data

    def calculate(self):

        total = len(self.stocks)

        advancing = 0
        declining = 0

        above20 = 0
        above50 = 0
        above200 = 0

        for stock in self.stocks:

            close = stock["close"]

            ema20 = stock["ema20"]
            ema50 = stock["ema50"]
            ema200 = stock["ema200"]

            if close > ema20:
                above20 += 1

            if close > ema50:
                above50 += 1

            if close > ema200:
                above200 += 1

            if close > ema50:
                advancing += 1
            else:
                declining += 1

        if declining == 0:
            adr = advancing
        else:
            adr = round(advancing / declining, 2)

        score = 0

        percent50 = (above50 / total) * 100

        if percent50 >= 80:
            score = 100

        elif percent50 >= 70:
            score = 85

        elif percent50 >= 60:
            score = 70

        elif percent50 >= 50:
            score = 55

        else:
            score = 30

        if score >= 85:
            health = "VERY_STRONG"

        elif score >= 70:
            health = "STRONG"

        elif score >= 55:
            health = "NEUTRAL"

        else:
            health = "WEAK"

        return MarketBreadthResult(

            total_stocks=total,

            advancing=advancing,

            declining=declining,

            advance_decline_ratio=adr,

            above_20ema=above20,

            above_50ema=above50,

            above_200ema=above200,

            breadth_score=score,

            market_health=health,
        )