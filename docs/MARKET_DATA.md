# Market Data Module

## Provider

Yahoo Finance

## Supported Universes

- Nifty 50
- Nifty 100
- Nifty 200
- Nifty 500
- NSE All
- Custom Watchlists

## Supported Timeframes

- Daily
- 1 Hour
- 30 Minutes
- 15 Minutes
- 5 Minutes

## Components

- YahooFinanceProvider
- MarketDataService
- HistoricalLoader
- LiveLoader
- SymbolManager
- CacheManager
- TimeframeManager
- DataValidator

## Usage

1. Load watchlist
2. Download historical data
3. Validate data
4. Cache data
5. Send to Scanner Engine
