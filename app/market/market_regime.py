from dataclasses import dataclass


@dataclass
class MarketRegime:
    regime: str
    score: int
    buy_allowed: bool
    watch_allowed: bool
    risk_multiplier: float
    max_positions: int
    allowed_strategies: list


class MarketRegimeEngine:

    def __init__(
        self,
        weekly_trend: str,
        daily_trend: str,
        adx: float,
        breadth: float,
        vix: float,
        distribution_days: int,
        sector_strength: float,
    ):

        self.weekly_trend = weekly_trend.upper()
        self.daily_trend = daily_trend.upper()
        self.adx = adx
        self.breadth = breadth
        self.vix = vix
        self.distribution_days = distribution_days
        self.sector_strength = sector_strength

    def evaluate(self):

        score = 0

        # Weekly Trend
        if self.weekly_trend == "BULLISH":
            score += 30
        elif self.weekly_trend == "SIDEWAYS":
            score += 15

        # Daily Trend
        if self.daily_trend == "BULLISH":
            score += 25
        elif self.daily_trend == "SIDEWAYS":
            score += 10

        # ADX
        if self.adx >= 30:
            score += 15
        elif self.adx >= 25:
            score += 12
        elif self.adx >= 20:
            score += 8

        # Breadth
        if self.breadth >= 75:
            score += 15
        elif self.breadth >= 60:
            score += 10
        elif self.breadth >= 50:
            score += 5

        # Sector Strength
        if self.sector_strength >= 70:
            score += 10
        elif self.sector_strength >= 50:
            score += 5

        # India VIX
        if self.vix < 15:
            score += 10
        elif self.vix < 18:
            score += 8
        elif self.vix < 22:
            score += 5

        # Distribution Days
        if self.distribution_days >= 5:
            score -= 20
        elif self.distribution_days >= 3:
            score -= 10

        score = max(0, min(score, 100))

        print(f"[Market Regime] Score={score}")