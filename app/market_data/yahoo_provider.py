from __future__ import annotations

from typing import Optional

import yfinance as yf

from .base_provider import MarketDataProvider
from .exceptions import (
    EmptyDataError,
    InvalidSymbolError,
    ProviderConnectionError,
)
from .models import MarketData
from .utils import now, validate_interval


class YahooFinanceProvider(MarketDataProvider):
    """
    Yahoo Finance Market Data Provider
    """

    def history(
        self,
        symbol: str,
        interval: str = "1d",
        period: str = "6mo"
    ) -> MarketData:

        validate_interval(interval)

        try:

            df = yf.download(
                tickers=symbol,
                interval=interval,
                period=period,
                progress=False,
                auto_adjust=True,
                threads=False
            )

        except Exception as e:

            raise ProviderConnectionError(str(e))

        if df is None or df.empty:
            raise EmptyDataError(f"No data found for {symbol}")

        return MarketData(
            symbol=symbol,
            timeframe=interval,
            data=df,
            downloaded_at=now()
        )

    def latest_price(self, symbol: str) -> float:

        try:

            ticker = yf.Ticker(symbol)

            info = ticker.fast_info

            price: Optional[float] = info.get("lastPrice")

            if price is None:
                raise InvalidSymbolError(symbol)

            return float(price)

        except Exception as e:
            raise ProviderConnectionError(str(e))
