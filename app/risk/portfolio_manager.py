from dataclasses import dataclass


@dataclass
class PortfolioResult:

    total_positions: int

    open_risk: float

    exposure_percent: float

    sector_exposure: dict

    allow_new_trade: bool

    reason: str


class PortfolioManager:

    def __init__(

        self,

        capital,

        max_positions=10,

        max_exposure=80,

        max_sector_exposure=30,

    ):

        self.capital = capital

        self.max_positions = max_positions

        self.max_exposure = max_exposure

        self.max_sector_exposure = max_sector_exposure

    def evaluate(

        self,

        positions,

    ):

        total_positions = len(positions)

        invested = 0

        sector_data = {}

        for position in positions:

            invested += position["value"]

            sector = position["sector"]

            sector_data[sector] = sector_data.get(

                sector,

                0,

            ) + position["value"]

        exposure = (

            invested /

            self.capital

        ) * 100

        if total_positions >= self.max_positions:

            return PortfolioResult(

                total_positions,

                invested,

                exposure,

                sector_data,

                False,

                "Maximum Positions Reached",

            )

        if exposure >= self.max_exposure:

            return PortfolioResult(

                total_positions,

                invested,

                exposure,

                sector_data,

                False,

                "Portfolio Fully Invested",

            )

        for sector, value in sector_data.items():

            sector_percent = (

                value /

                self.capital

            ) * 100

            if sector_percent >= self.max_sector_exposure:

                return PortfolioResult(

                    total_positions,

                    invested,

                    exposure,

                    sector_data,

                    False,

                    f"Sector Limit Exceeded ({sector})",

                )

        return PortfolioResult(

            total_positions,

            invested,

            exposure,

            sector_data,

            True,

            "Portfolio Healthy",

        )