from app.market_data.yahoo_provider import YahooFinanceProvider
from app.market_data.market_data_service import MarketDataService

from app.scanner.indicator_engine import IndicatorEngine
from app.telegram.chart_generator import ChartGenerator

provider = YahooFinanceProvider()

service = MarketDataService(provider)

market = service.get_daily("BEL.NS")

df = market.data.copy()

df["EMA20"] = IndicatorEngine.ema(df, 20)

df["EMA50"] = IndicatorEngine.ema(df, 50)

df["EMA200"] = IndicatorEngine.ema(df, 200)

chart = ChartGenerator()

print(chart.generate(df, "BEL.NS"))
