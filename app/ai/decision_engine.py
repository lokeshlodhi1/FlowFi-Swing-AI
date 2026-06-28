import json
from pathlib import Path


class DecisionEngine:
    """
    Combines feature scores using configurable weights
    and returns the final trading decision.
    """

    def __init__(self):
        config_path = Path("config/scoring.json")

        if config_path.exists():
            with open(config_path, "r") as file:
                self.weights = json.load(file)
        else:
            self.weights = {
                "market": 20,
                "sector": 15,
                "ema": 15,
                "volume": 10,
                "relative_strength": 15,
                "candlestick": 10,
                "timeframe": 15
            }

    def score(self, features):

        total_weight = sum(self.weights.values())

        weighted_score = 0

        for key, weight in self.weights.items():

            value = features.get(key, 0)

            weighted_score += (value / 100) * weight

        final_score = round((weighted_score / total_weight) * 100, 2)

        if final_score >= 90:
            signal = "BUY"

        elif final_score >= 80:
            signal = "WATCH"

        else:
            signal = "IGNORE"

        return {
            "score": final_score,
            "signal": signal
        }
