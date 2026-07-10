import json
from pathlib import Path


class DecisionEngine:
    """
    FlowFi AI Swing Trading Strategy v2.0 - Decision Engine
    Combines institutional feature scores using weighted allocation.
    """

    def __init__(self):
        config_path = Path("config/scoring.json")

        if config_path.exists():
            try:
                with open(config_path, "r") as file:
                    self.weights = json.load(file)
            except Exception:
                self._load_v2_default_weights()
        else:
            self._load_v2_default_weights()

    def _load_v2_default_weights(self):
        # Explicit Strategy v2.0 Weight Allocations
        self.weights = {
            "market": 20,       # Market Analysis (20%)
            "stock": 20,        # Stock Quality Filter (20%)
            "strategy": 20,     # Strategy Specific Execution (20%)
            "volume": 15,       # Volume Confirmation (15%)
            "momentum": 15,     # Momentum/RSI Indicators (15%)
            "risk": 10          # Risk Reward Ratio (10%)
        }

    def score(self, features):
        total_weight = sum(self.weights.values())
        weighted_score = 0

        # Calculate institutional scores dynamically based on v2.0 rules
        for key, weight in self.weights.items():
            value = features.get(key, 0)
            # Ensure safe bounding between 0 and 100 for input values
            value = max(0, min(100, value)) 
            weighted_score += (value / 100) * weight

        # Generate final percentage score
        final_score = round((weighted_score / total_weight) * 100, 2)

        # Strategy v2.0 Final Decision Thresholds
        if final_score >= 90:
            signal = "STRONG BUY"
        elif final_score >= 75:
            signal = "BUY"
        elif final_score >= 60:
            signal = "WATCH"
        else:
            signal = "REJECT"

        return {
            "score": final_score,
            "signal": signal
        }
