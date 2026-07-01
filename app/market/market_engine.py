from app.market.market_trend import MarketTrend
from app.market.market_regime import MarketRegimeEngine
from app.market.distribution_days import DistributionDays


class MarketEngine:

    def __init__(self):

        self.market_trend = MarketTrend()

    def analyse_market(self):

        trend = self.market_trend.get_trend()

        # Temporary values
        # These will come from the new modules in the next phase

        breadth_score = 80
        sector_strength = 75
        vix = 15
        adx = 28
        distribution_days = 2

        regime = MarketRegimeEngine(
            weekly_trend=trend.trend,
            daily_trend=trend.trend,
            adx=adx,
            breadth=breadth_score,
            vix=vix,
            distribution_days=distribution_days,
            sector_strength=sector_strength,
        ).evaluate()

        return {

            "market_trend": trend,

            "market_regime": regime,

            "buy_allowed": regime.buy_allowed,

            "watch_allowed": regime.watch_allowed,

            "risk_multiplier": regime.risk_multiplier,

            "max_positions": regime.max_positions,

            "allowed_strategies": regime.allowed_strategies,

        }