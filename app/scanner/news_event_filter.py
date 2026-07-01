from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class NewsFilterResult:

    passed: bool

    reason: str

    hours_remaining: float


class NewsEventFilter:

    def __init__(self):

        pass

    def evaluate(

        self,

        earnings_date=None,

        event_date=None,

    ):

        now = datetime.now()

        # Earnings Filter

        if earnings_date is not None:

            hours = (

                earnings_date - now

            ).total_seconds() / 3600

            if 0 <= hours <= 48:

                return NewsFilterResult(

                    False,

                    "Upcoming Earnings",

                    round(hours, 2),

                )

        # Major Event Filter

        if event_date is not None:

            hours = (

                event_date - now

            ).total_seconds() / 3600

            if 0 <= hours <= 24:

                return NewsFilterResult(

                    False,

                    "Major Market Event",

                    round(hours, 2),

                )

        return NewsFilterResult(

            True,

            "No Major Events",

            0,

        )