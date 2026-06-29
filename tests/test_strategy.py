from app.strategies.market_filter import MarketFilter
from app.strategies.trend_filter import TrendFilter
from app.strategies.ema_pullback import EMAPullback
from app.strategies.volume_confirmation import VolumeConfirmation

market = MarketFilter()
trend = TrendFilter()
ema = EMAPullback()
volume = VolumeConfirmation()

print("Market:", market.is_bullish(25000, 24800))
print("Trend:", trend.bullish(520, 500, 470))
print("EMA Pullback:", ema.bullish(100, 100.5))
print("Relative Volume:", volume.relative_volume(2500000, 1000000))
print("Volume Valid:", volume.is_valid(2500000, 1000000))
