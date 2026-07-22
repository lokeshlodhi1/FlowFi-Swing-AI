import os
from app.market_data import (
    YahooFinanceProvider,
    MarketDataService,
    SymbolManager,
)
from app.scanner.scanner_executor import ScannerExecutor
from app.database.database_service import DatabaseService
from app.telegram.telegram_service import TelegramService
from config import config

# --- NEW TRACKING IMPORTS ---
from app.scanner.trade_manager import TradeManager
from app.scanner.trade_journal import TradeJournal

class FlowFIRunner:

    def __init__(self):
        self.provider = YahooFinanceProvider()
        self.market = MarketDataService(self.provider)
        self.symbols = SymbolManager()
        self.scanner = ScannerExecutor()
        self.database = DatabaseService()
        self.telegram = TelegramService(
            config.TELEGRAM_TOKEN,
            config.TELEGRAM_CHAT_ID,
        )
        
        # --- NEW TRACKING INITIALIZATION ---
        self.trade_manager = TradeManager()
        os.makedirs("data", exist_ok=True)
        # Keeps your structural strategy metrics isolated cleanly in Excel
        self.journal = TradeJournal(filepath="data/ema_pullback_journal.xlsx")

    def monitor_active_positions(self):
        """
        Fetches live open positions from the database, runs target/SL analysis,
        and coordinates spreadsheet saving with live Telegram alerts.
        """
        print("\n" + "=" * 60)
        print("MONITORING LIVE TRACKED POSITIONS (SL / TARGET CHECK)")
        print("=" * 60)
        
        # Pull dynamic positions currently flagged as active in your DB framework
        # NOTE: Make sure your trade repository object supports retrieving open positions.
        # If the method name differs slightly in your db code, adjust 'get_open_positions()' accordingly.
        if not hasattr(self.database.trades, 'get_open_positions'):
            print("⚠️ 'get_open_positions' method not detected on database class. Skipping monitoring loop.")
            return
            
        open_trades = self.database.trades.get_open_positions()
        
        if not open_trades:
            print("No active open positions to track.\n")
            return

        for trade in open_trades:
            symbol = trade.get("symbol")
            
            try:
                # 1. Grab fresh price data using your internal market loader module
                # Pulls structural quote history or current ticker price
                price_data = self.market.get_live_price(symbol)
                if not price_data:
                    continue
                
                # 2. Run data metrics through your optimized TradeManager calculation engine
                result = self.trade_manager.update(
                    symbol=symbol,
                    entry=float(trade.get("entry_price")),
                    stop_loss=float(trade.get("stop_loss")),
                    target1=float(trade.get("target1")),
                    target2=float(trade.get("target2")),
                    current_price=float(price_data)
                )
                
                # 3. Handle exit logic structural changes
                if result.status != "OPEN":
                    # Update local Excel sheet tracker logs
                    self.journal.update_status(
                        symbol=result.symbol,
                        status=result.status,
                        exit_price=result.current_price
                    )
                    
                    # Update central database records
                    self.database.trades.update_trade_status(symbol, status=result.status, close_price=result.current_price)
                    
                    # Map message visual emojis based on target outcomes
                    alert_emojis = {
                        "TARGET1_HIT": "🎯 Target 1 Achieved! 🟢",
                        "TARGET2_HIT": "🚀 Target 2 Smashed! 🎉",
                        "SL_EXIT": "🚨 Stop Loss Triggered 🔴",
                        "TRAILING_SL_EXIT": "🛡️ Trailing Stop Hit 🟡"
                    }
                    
                    alert_msg = (
                        f"{alert_emojis.get(result.status, '⚠️ Position Update')}\n\n"
                        f"**Stock:** {result.symbol}\n"
                        f"**Current Price:** {result.current_price}\n"
                        f"**P&L:** {result.pnl_percent}%\n"
                        f"**Trailing SL Settled:** {result.trailing_stop}"
                    )
                    
                    # 4. Broadcast instant notification reply right to Telegram group channels
                    self.telegram.send_message(alert_msg)
                    print(f"📊 Position structural status shift processed for {symbol}: {result.status}")

            except Exception as e:
                print(f"❌ Error monitoring position {symbol}: {e}")
        print("=" * 60 + "\n")

    def run(self):
        # --- NEW STEP: Run position monitoring logic before running the new scan loop ---
        self.monitor_active_positions()

        nifty50 = self.symbols.load("nifty50")
        midcap100 = self.symbols.load("niftymidcap100")

        stocks = list(dict.fromkeys(nifty50 + midcap100))

        print("=" * 60)
        print("FLOWFI AI SCANNER")
        print("=" * 60)
        print(f"Scanning {len(stocks)} Stocks...\n")

        total = 0
        saved = 0

        for symbol in stocks:
            total += 1
            try:
                trade = self.scanner.scan_stock(symbol)

                if trade is None:
                    continue

                # Skip rejected and watch signals
                if trade.get("signal") not in ["BUY", "STRONG BUY"]:
                    print(
                        f"❌ {symbol} : "
                        f"{trade.get('reason','Rejected')}"
                    )
                    continue

                print(trade)

                # -----------------------------
                # Save Database
                # -----------------------------
                try:
                    self.database.trades.add_trade(trade)
                    print("✅ Saved to Database")
                    
                    # Also log the initial trade structure into Excel tracker sheet right away
                    trade_log = {
                        "Ticker": trade.get("symbol"),
                        "Entry Price": trade.get("entry"),
                        "Stop Loss": trade.get("stop_loss"),
                        "Target": trade.get("target1"), # or log map arrays directly
                        "Status": "OPEN"
                    }
                    self.journal.add_entry(trade_log)
                    
                    saved += 1
                except Exception as db_error:
                    print(f"❌ Database Error: {db_error}")

                # -----------------------------
                # Telegram
                # -----------------------------
                try:
                    sent = self.telegram.send_trade(trade)
                    if sent:
                        print("📨 Telegram Sent")
                    else:
                        print("❌ Telegram Not Sent")
                except Exception as tg_error:
                    print(f"❌ Telegram Error: {tg_error}")

            except Exception as e:
                print(f"❌ {symbol}: {e}")

        print()
        print("=" * 60)
        print("SCAN COMPLETED")
        print("=" * 60)
        print(f"Stocks Scanned : {total}")
        print(f"Trades Saved   : {saved}")
        print("=" * 60)
