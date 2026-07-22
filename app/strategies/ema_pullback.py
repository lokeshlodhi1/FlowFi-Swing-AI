import os
from datetime import datetime
from app.strategies.market_filter import MarketFilter  # Assuming base class structures if any
from app.scanner.trade_journal import TradeJournal[cite: 1]
from app.database.pnl_calculator import PnLCalculator[cite: 1]
from app.telegram.telegram_service import TelegramService[cite: 1]
from app.telegram.message_formatter import MessageFormatter[cite: 1]

class EMAPullbackStrategy:
    def __init__(self, config=None):
        self.config = config or {}
        self.strategy_name = "EMA_Pullback"
        
        # 1. Initialize Excel Logging & Tracking
        # Saves logs specifically for this strategy to avoid cluttering your breakout files
        os.makedirs("data", exist_ok=True)
        self.journal = TradeJournal(filepath="data/ema_pullback_journal.xlsx")
        self.pnl_calc = PnLCalculator()
        
        # 2. Initialize Telegram Notifications
        self.telegram_service = TelegramService()
        self.formatter = MessageFormatter()

    def scan_and_execute(self, ticker, data):
        """
        Main logic loop executed by runner.py / scanner_executor.py
        """
        # --- YOUR EXISTING TECHNICAL INDICATOR LOGIC HERE ---
        # (e.g., checking if price pulled back to the 20 EMA, volume confirmation, etc.)
        is_signal_valid = True  # Placeholder for your logic evaluation
        entry_price = 100.0      # Placeholder
        sl_price = 95.0          # Placeholder 
        target_price = 110.0      # Placeholder
        # ----------------------------------------------------

        if is_signal_valid:
            self.handle_entry(ticker, entry_price, sl_price, target_price)

    def handle_entry(self, ticker, entry_price, sl_price, target_price):
        """
        Logs the entry to Excel and broadcasts a Telegram notification
        """
        trade_data = {
            "Ticker": ticker,
            "Strategy": self.strategy_name,
            "Entry Price": entry_price,
            "Stop Loss": sl_price,
            "Target": target_price,
            "Status": "OPEN",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Write to spreadsheet
        self.journal.add_entry(trade_data)
        
        # Dispatch Telegram Alert for a new setup
        if hasattr(self.formatter, 'format_entry_alert'):
            msg = self.formatter.format_entry_alert(ticker, "BUY", entry_price, sl_price, target_price)
            self.telegram_service.send_message(msg)

    def monitor_positions(self, ticker, current_price, entry_price, sl_price, target_price):
        """
        Call this method on your active watchlists to automatically process 
        exits, update Excel tracking rows, and blast Telegram replies.
        """
        # 1. Check if Stop Loss is Breached
        if current_price <= sl_price:
            pnl_pct = ((current_price - entry_price) / entry_price) * 100
            
            # Update Excel Journal status
            self.journal.update_status(ticker, status="SL_HIT", exit_price=current_price)
            
            # Construct and fire Telegram warning
            message = (
                f"🚨 **{ticker} - STOP LOSS HIT** 🚨\n\n"
                f"Strategy: {self.strategy_name}\n"
                f"Entry Price: {entry_price}\n"
                f"Exit Price: {current_price}\n"
                f"Loss: {pnl_pct:.2f}%"
            )
            self.telegram_service.send_message(message)
            return "CLOSED"

        # 2. Check if Target is Secured
        elif current_price >= target_price:
            pnl_pct = ((current_price - entry_price) / entry_price) * 100
            
            # Update Excel Journal status
            self.journal.update_status(ticker, status="TARGET_HIT", exit_price=current_price)
            
            # Construct and fire Telegram celebration alert
            message = (
                f"🎯 **{ticker} - TARGET HIT** 🎉\n\n"
                f"Strategy: {self.strategy_name}\n"
                f"Entry Price: {entry_price}\n"
                f"Exit Price: {current_price}\n"
                f"Profit: +{pnl_pct:.2f}%"
            )
            self.telegram_service.send_message(message)
            return "CLOSED"
            
        return "OPEN"
