from dataclasses import dataclass


@dataclass
class MultiTimeframeResult:

    weekly: bool

    daily: bool

    h4: bool

    h2: bool

    score: int

    passed: bool

    trend: str


class MultiTimeframe:

    def confirm(

        self,

        weekly,

        daily,

        h4,

        h2,

    ):

        score = 0

        if weekly:
            score += 30

        if daily:
            score += 30

        if h4:
            score += 25

        if h2:
            score += 15

        if score >= 90:

            trend = "STRONG_BULL"

        elif score >= 70:

            trend = "BULLISH"

        elif score >= 50:

            trend = "NEUTRAL"

        else:

            trend = "BEARISH"

        return MultiTimeframeResult(

            weekly=weekly,

            daily=daily,

            h4=h4,

            h2=h2,

            score=score,

            passed=score >= 70,

            trend=trend,

        )