class TimeframeManager:

    INTERVALS = {

        "daily": "1d",

        "4h": "1h",

        "2h": "1h",

        "1h": "1h",

        "30m": "30m",

        "15m": "15m",

        "5m": "5m"

    }

    @classmethod
    def get(cls, timeframe):

        return cls.INTERVALS[timeframe]

    @classmethod
    def supported(cls):

        return list(cls.INTERVALS.keys())
