from typing import Dict

from .market_data_service import MarketDataService


class HistoricalLoader:
    """
    Loads historical market data for multiple symbols.
    """

    def __init__(self, service: MarketDataService):
        self.service = service

    def load(
        self,
        symbols: list[str],
        interval: str = "1d",
        period: str = "6mo"
    ) -> Dict:

        result = {}

        for symbol in symbols:

            try:

                result[symbol] = self.service.provider.history(
                    symbol=symbol,
                    interval=interval,
                    period=period
                )

            except Exception as e:

                print(f"{symbol}: {e}")

        return result
