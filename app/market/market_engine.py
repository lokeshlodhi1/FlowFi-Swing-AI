from app.market.market_trend import MarketTrend


class MarketEngine:

    def __init__(self):
        self.market_trend = MarketTrend()

    def get_market_status(self):

        trend = self.market_trend.get_trend()

        market_status = {
            "trend": trend.trend,
            "trend_strength": trend.trend_strength,
            "buy_allowed": False,
            "watch_allowed": False,
            "risk_level": "LOW",
            "position_size": 0.0,
        }

        # Strong Bull Market
        if (
            trend.trend == "BULLISH"
            and trend.bullish_alignment
            and trend.trend_strength >= 100
        ):
            market_status["buy_allowed"] = True
            market_status["watch_allowed"] = True
            market_status["risk_level"] = "HIGH"
            market_status["position_size"] = 1.0

        # Bull Market
        elif (
            trend.trend == "BULLISH"
            and trend.trend_strength >= 75
        ):
            market_status["buy_allowed"] = True
            market_status["watch_allowed"] = True
            market_status["risk_level"] = "MEDIUM"
            market_status["position_size"] = 0.75

        # Sideways Market
        elif trend.trend == "SIDEWAYS":
            market_status["buy_allowed"] = False
            market_status["watch_allowed"] = True
            market_status["risk_level"] = "LOW"
            market_status["position_size"] = 0.25

        # Bear Market
        else:
            market_status["buy_allowed"] = False
            market_status["watch_allowed"] = False
            market_status["risk_level"] = "NONE"
            market_status["position_size"] = 0.0

        return market_status