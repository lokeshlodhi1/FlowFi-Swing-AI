from app.market_data import (
    YahooFinanceProvider,
    MarketDataService,
    SymbolManager,
)

from app.scanner.scanner_executor import ScannerExecutor
from app.database.database_service import DatabaseService
from app.telegram.telegram_service import TelegramService
from config import config
from app.market import MarketTrend

class FlowFIRunner:

    def __init__(self):

        self.provider = YahooFinanceProvider()

        self.market = MarketDataService(self.provider)

        self.symbols = SymbolManager()

        self.scanner = ScannerExecutor()

        self.database = DatabaseService()

        self.telegram = TelegramService(
            config.TELEGRAM_TOKEN,
            config.TELEGRAM_CHAT_ID
        )

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
                    continue

                print(trade)

                # Save to Database
                try:
                    self.database.trades.add_trade(trade)
                    print("✅ Saved to Database")

                except Exception as db_error:
                    print(f"❌ Database Error: {db_error}")

                # Send Telegram
                try:
                    self.telegram.send_trade(trade)
                    print("📨 Telegram Sent")

                except Exception as tg_error:
                    print(f"❌ Telegram Error: {tg_error}")

                saved += 1

            except Exception as e:

                print(f"❌ {symbol}: {e}")

        print("\n" + "=" * 60)
        print("SCAN COMPLETED")
        print("=" * 60)
        print(f"Stocks Scanned : {total}")
        print(f"Trades Saved   : {saved}")
        print("=" * 60)
