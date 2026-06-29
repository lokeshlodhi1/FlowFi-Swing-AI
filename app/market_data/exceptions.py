class MarketDataError(Exception):
    """Base market data exception."""


class ProviderConnectionError(MarketDataError):
    """Raised when provider connection fails."""


class InvalidSymbolError(MarketDataError):
    """Raised when symbol is invalid."""


class InvalidTimeframeError(MarketDataError):
    """Raised when timeframe is invalid."""


class EmptyDataError(MarketDataError):
    """Raised when provider returns no data."""
