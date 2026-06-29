from dataclasses import dataclass
import os

@dataclass
class Config:

    # Scanner
    SCAN_UNIVERSE = "nifty50"
    CAPITAL = 100000
    RISK_PERCENT = 1
    MIN_AI_SCORE = 90

    # Strategy
    EMA = 20
    VOLUME_RATIO = 1.5

    # Telegram
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

    # Database
    DATABASE = "flowfi.db"

    # Market
    PERIOD = "6mo"
    INTERVAL = "1d"


config = Config()

print("\n========== CONFIG ==========")
print("Token Exists :", bool(config.TELEGRAM_TOKEN))
print("Chat ID Len  :", len(config.TELEGRAM_CHAT_ID))
print("Chat ID Ends :", config.TELEGRAM_CHAT_ID[-4:] if config.TELEGRAM_CHAT_ID else "EMPTY")
print("============================\n")
