from datetime import datetime


SUPPORTED_INTERVALS = {

    "1d",

    "1h",

    "30m",

    "15m",

    "5m"

}


def now():

    return datetime.now()


def validate_interval(interval: str):

    if interval not in SUPPORTED_INTERVALS:

        raise ValueError(

            f"Unsupported interval : {interval}"

        )
