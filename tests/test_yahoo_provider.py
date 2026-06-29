from app.market_data.market_data_service import MarketDataService
from app.market_data.yahoo_provider import YahooFinanceProvider

provider = YahooFinanceProvider()

service = MarketDataService(provider)

data = service.get_daily("RELIANCE.NS")

print(data.data.tail())

print(service.latest_price("RELIANCE.NS"))
