from app.strategies.market_filter import MarketFilter
from app.strategies.trend_filter import TrendFilter
from app.strategies.ema_pullback import EMAPullback
from app.strategies.volume_confirmation import VolumeConfirmation


class SignalGenerator:

    def __init__(self):

        self.market = MarketFilter()

        self.trend = TrendFilter()

        self.pullback = EMAPullback()

        self.volume = VolumeConfirmation()

    def generate(
        self,
        close,
        ema20,
        ema50,
        ema200,
        current_volume,
        avg_volume
    ):

        return {

            "market": True,

            "trend": self.trend.bullish(ema20, ema50, ema200),

            "ema": self.pullback.bullish(close, ema20),

            "volume": self.volume.is_valid(current_volume, avg_volume)

        }
