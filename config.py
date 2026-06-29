from dataclasses import dataclass
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

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

    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")

    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

    # Database

    DATABASE = "flowfi.db"

    # Market

    PERIOD = "6mo"

    INTERVAL = "1d"


config = Config()
