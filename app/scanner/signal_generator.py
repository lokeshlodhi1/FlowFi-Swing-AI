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

        result = {}

        # -------------------------
        # Market Filter
        # -------------------------
        result["market"] = True

        # -------------------------
        # Trend
        # -------------------------
        result["trend"] = self.trend.bullish(
            ema20,
            ema50,
            ema200
        )

        # -------------------------
        # EMA Pullback
        # -------------------------
        result["ema"] = self.pullback.bullish(
            close,
            ema20,
            tolerance=0.02
        )

        # -------------------------
        # Volume
        # -------------------------
        result["volume"] = self.volume.is_valid(
            current_volume,
            avg_volume
        )

        # -------------------------
        # AI Score
        # -------------------------
        score = 0

        if result["market"]:
            score += 20

        if result["trend"]:
            score += 20

        if result["ema"]:
            score += 30

        if result["volume"]:
            score += 30

        result["score"] = score

        # -------------------------
        # Decision
        # -------------------------
        if score >= 90:
            result["signal"] = "BUY"

        elif score >= 60:
            result["signal"] = "WATCH"

        else:
            result["signal"] = "IGNORE"

        result["confidence"] = score

        return result
