from __future__ import annotations

from .base_provider import MarketDataProvider
from .models import MarketData


class MarketDataService:
    """
    Main entry point for market data.
    """

    def __init__(self, provider: MarketDataProvider):

        self.provider = provider

    def get_daily(
        self,
        symbol: str,
        period: str = "6mo"
    ) -> MarketData:

        return self.provider.history(
            symbol=symbol,
            interval="1d",
            period=period
        )

    def get_4h(
        self,
        symbol: str,
        period: str = "6mo"
    ) -> MarketData:

        return self.provider.history(
            symbol=symbol,
            interval="1h",
            period=period
        )

    def get_2h(
        self,
        symbol: str,
        period: str = "6mo"
    ) -> MarketData:

        return self.provider.history(
            symbol=symbol,
            interval="1h",
            period=period
        )

    def get_15m(
        self,
        symbol: str,
        period: str = "5d"
    ) -> MarketData:

        return self.provider.history(
            symbol=symbol,
            interval="15m",
            period=period
        )

    def latest_price(
        self,
        symbol: str
    ) -> float:

        return self.provider.latest_price(symbol)
