from typing import Dict


class FeatureEngine:

    """
    Converts raw indicators into
    normalized feature scores (0-100)
    """

    def __init__(self):
        pass

    def ema_score(self, aligned: bool):

        return 100 if aligned else 0

    def market_score(self, bullish: bool):

        return 100 if bullish else 0

    def sector_score(self, strength: float):

        return min(100, max(0, strength))

    def volume_score(self, relative_volume: float):

        score = relative_volume * 50

        return min(100, round(score))

    def relative_strength_score(self, rs: float):

        score = 50 + rs * 5

        return min(100, max(0, round(score)))

    def candle_score(self, confirmed: bool):

        return 100 if confirmed else 0

    def timeframe_score(self, score: int):

        return score

    def build(self, data: Dict):

        return {

            "market": self.market_score(data["market"]),

            "sector": self.sector_score(data["sector"]),

            "ema": self.ema_score(data["ema"]),

            "volume": self.volume_score(data["volume"]),

            "relative_strength": self.relative_strength_score(
                data["relative_strength"]
            ),

            "candlestick": self.candle_score(
                data["candlestick"]
            ),

            "timeframe": self.timeframe_score(
                data["timeframe"]
            )

        }
