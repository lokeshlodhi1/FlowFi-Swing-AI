# test_strategy_alerts.py
from app.strategies.ema_pullback import EMAPullbackStrategy

print("Initializing test strategy verification...")
test_strat = EMAPullbackStrategy()

print("Testing Excel log entry and entry Telegram alert...")
test_strat.handle_entry(ticker="TEST_STOCK", entry_price=100, sl_price=95, target_price=110)

print("Simulating a Target Hit event...")
test_strat.monitor_positions(ticker="TEST_STOCK", current_price=112, entry_price=100, sl_price=95, target_price=110)

print("Test complete! Check your Excel file and Telegram group for confirmation updates.")
