from app.scanner.advanced_indicator import AdvancedIndicator
from app.scanner.multi_timeframe import MultiTimeframe
from app.scanner.market_strength import MarketStrength
from app.scanner.sector_strength import SectorStrength

import pandas as pd

# Dummy Data
df = pd.DataFrame({
    "Open": [100, 101, 102, 103, 104, 105, 106, 107, 108, 109,
             110,111,112,113,114,115,116,117,118,119],
    "High": [101,102,103,104,105,106,107,108,109,110,
             111,112,113,114,115,116,117,118,119,120],
    "Low": [99,100,101,102,103,104,105,106,107,108,
            109,110,111,112,113,114,115,116,117,118],
    "Close": [100,101,102,103,104,105,106,107,108,109,
              110,111,112,113,114,115,116,117,118,119],
    "Volume": [100000] * 20
})

indicator = AdvancedIndicator()

print("RSI")
print(indicator.rsi(df).tail())

print("\nMACD")
macd, signal = indicator.macd(df)
print(macd.tail())
print(signal.tail())

print("\nVWAP")
print(indicator.vwap(df).tail())

market = MarketStrength()
print("\nMarket:", market.score(25100, 24800))

sector = SectorStrength()
print("Sector:", sector.strongest(3))

mtf = MultiTimeframe()
print("MTF:", mtf.confirm(True, True, True))
