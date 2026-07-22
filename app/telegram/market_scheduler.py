from datetime import datetime
from app.strategies.ema_pullback import EMAPullbackStrategy


class MarketScheduler:

    SCAN_TIMES = [

        "09:20",

        "10:00",

        "11:00",

        "12:00",

        "13:00",

        "14:00",

        "15:00"

    ]

    def should_scan(self):

        now = datetime.now().strftime("%H:%M")

        return now in self.SCAN_TIMES
