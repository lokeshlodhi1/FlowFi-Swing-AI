from dataclasses import dataclass

import pandas as pd


@dataclass
class DistributionDayResult:
    distribution_days: int
    accumulation_days: int
    market_condition: str


class DistributionDays:

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()

    def calculate(self) -> DistributionDayResult:

        df = self.df.tail(25).copy()

        distribution = 0
        accumulation = 0

        for i in range(1, len(df)):

            prev_close = df["Close"].iloc[i - 1]
            curr_close = df["Close"].iloc[i]

            prev_volume = df["Volume"].iloc[i - 1]
            curr_volume = df["Volume"].iloc[i]

            # Distribution Day
            if (
                curr_close < prev_close
                and curr_volume > prev_volume
            ):
                distribution += 1

            # Accumulation Day
            elif (
                curr_close > prev_close
                and curr_volume > prev_volume
            ):
                accumulation += 1

        # Market Classification

        if distribution <= 2:
            market = "HEALTHY"

        elif distribution <= 4:
            market = "CAUTION"

        elif distribution <= 6:
            market = "WEAK"

        else:
            market = "DISTRIBUTION"

        return DistributionDayResult(
            distribution_days=distribution,
            accumulation_days=accumulation,
            market_condition=market,
        )