from app.market_data import (
    YahooFinanceProvider,
    MarketDataService,
    HistoricalLoader,
    LiveLoader,
    SymbolManager
)

provider = YahooFinanceProvider()

service = MarketDataService(provider)

symbols = SymbolManager().load("nifty50")

history = HistoricalLoader(service)

data = history.load(symbols[:5])

print(data.keys())

live = LiveLoader(service)

print(live.latest_prices(symbols[:5]))
