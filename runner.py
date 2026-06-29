from app.market_data import (
    YahooFinanceProvider,
    MarketDataService,
    SymbolManager,
)

from app.scanner.scanner_executor import ScannerExecutor


class FlowFIRunner:

    def __init__(self):

        self.provider = YahooFinanceProvider()

        self.market = MarketDataService(self.provider)

        self.symbols = SymbolManager()

        self.scanner = ScannerExecutor()

    def run(self):

        stocks = self.symbols.load("nifty50")

        print("=" * 60)
        print("FLOWFI AI SCANNER")
        print("=" * 60)

        print(f"Scanning {len(stocks)} Stocks...\n")

        for symbol in stocks:

            try:

                trade = self.scanner.scan(symbol)

                print(trade)

            except Exception as e:

                print(symbol, e)

        print("\nScan Finished")
