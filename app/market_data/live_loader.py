from typing import Dict

from .market_data_service import MarketDataService


class LiveLoader:

    def __init__(self, service: MarketDataService):

        self.service = service

    def latest_prices(
        self,
        symbols: list[str]
    ) -> Dict[str, float]:

        prices = {}

        for symbol in symbols:

            try:

                prices[symbol] = self.service.latest_price(symbol)

            except Exception:

                prices[symbol] = None

        return prices
