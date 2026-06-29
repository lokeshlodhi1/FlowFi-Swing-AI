from app.market_data import (
    YahooFinanceProvider,
    MarketDataService,
    SymbolManager,
)

from app.scanner.scanner_executor import ScannerExecutor
from app.database.database_service import DatabaseService


class FlowFIRunner:

    def __init__(self):

        self.provider = YahooFinanceProvider()

        self.market = MarketDataService(self.provider)

        self.symbols = SymbolManager()

        self.scanner = ScannerExecutor()

        self.database = DatabaseService()

    def run(self):

        stocks = self.symbols.load("nifty50")

        print("=" * 60)
        print("FLOWFI AI SCANNER")
        print("=" * 60)

        print(f"Scanning {len(stocks)} Stocks...\n")

        total = 0
        saved = 0

        for symbol in stocks:

            total += 1

            try:

                trade = self.scanner.scan(symbol)

                if trade is None:
                    print(f"{symbol} : No Trade")
                    continue

                print(trade)

                try:
                    self.database.trades.add_trade(trade)
                    print("✅ Saved to Database")
                    saved += 1
                except Exception as db_error:
                    print(f"❌ Database Error : {db_error}")

            except Exception as e:

                print(f"❌ {symbol} : {e}")

        print("\n" + "=" * 60)
        print("SCAN COMPLETED")
        print("=" * 60)
        print(f"Stocks Scanned : {total}")
        print(f"Trades Saved   : {saved}")
        print("=" * 60)from app.market_data import (
    YahooFinanceProvider,
    MarketDataService,
    SymbolManager,
)

from app.scanner.scanner_executor import ScannerExecutor
from app.database.database_service import DatabaseService


class FlowFIRunner:

    def __init__(self):

        self.provider = YahooFinanceProvider()

        self.market = MarketDataService(self.provider)

        self.symbols = SymbolManager()

        self.scanner = ScannerExecutor()

        self.database = DatabaseService()

    def run(self):

        stocks = self.symbols.load("nifty50")

        print("=" * 60)
        print("FLOWFI AI SCANNER")
        print("=" * 60)

        print(f"Scanning {len(stocks)} Stocks...\n")

        total = 0
        saved = 0

        for symbol in stocks:

            total += 1

            try:

                trade = self.scanner.scan(symbol)

                if trade is None:
                    print(f"{symbol} : No Trade")
                    continue

                print(trade)

                try:
                    self.database.trades.add_trade(trade)
                    print("✅ Saved to Database")
                    saved += 1
                except Exception as db_error:
                    print(f"❌ Database Error : {db_error}")

            except Exception as e:

                print(f"❌ {symbol} : {e}")

        print("\n" + "=" * 60)
        print("SCAN COMPLETED")
        print("=" * 60)
        print(f"Stocks Scanned : {total}")
        print(f"Trades Saved   : {saved}")
        print("=" * 60)
