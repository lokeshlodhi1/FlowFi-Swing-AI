from dataclasses import dataclass


@dataclass
class SectorResult:

    sector: str

    score: int

    rank: int

    momentum: str

    passed: bool


class SectorRotation:

    def __init__(

        self,

        sector_name,

        sector_return,

        nifty_return,

    ):

        self.sector = sector_name

        self.sector_return = sector_return

        self.nifty_return = nifty_return

    def evaluate(self):

        relative_strength = (

            self.sector_return -

            self.nifty_return

        )

        score = 50

        if relative_strength >= 8:

            score = 100

        elif relative_strength >= 6:

            score = 90

        elif relative_strength >= 4:

            score = 80

        elif relative_strength >= 2:

            score = 70

        elif relative_strength >= 0:

            score = 60

        else:

            score = 30

        if score >= 90:

            momentum = "VERY STRONG"

            rank = 1

        elif score >= 80:

            momentum = "STRONG"

            rank = 2

        elif score >= 70:

            momentum = "GOOD"

            rank = 3

        elif score >= 60:

            momentum = "AVERAGE"

            rank = 4

        else:

            momentum = "WEAK"

            rank = 5

        return SectorResult(

            sector=self.sector,

            score=score,

            rank=rank,

            momentum=momentum,

            passed=score >= 70,

        )