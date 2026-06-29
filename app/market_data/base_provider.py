from abc import ABC, abstractmethod

from .models import MarketData


class MarketDataProvider(ABC):

    @abstractmethod
    def history(
        self,
        symbol: str,
        interval: str,
        period: str
    ) -> MarketData:
        """
        Download historical OHLCV data.
        """

    @abstractmethod
    def latest_price(
        self,
        symbol: str
    ) -> float:
        """
        Latest traded price.
        """
