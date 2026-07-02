"""
Trading Configuration
Central place for all scanner settings.
"""

# -----------------------------
# Portfolio Settings
# -----------------------------

INITIAL_CAPITAL = 1_000_000

RISK_PERCENT = 1.0

MAX_OPEN_TRADES = 10

MAX_SIGNALS = 10

# -----------------------------
# EMA Settings
# -----------------------------

EMA_FAST = 20

EMA_MEDIUM = 50

EMA_SLOW = 200

# -----------------------------
# RSI Settings
# -----------------------------

RSI_MIN = 55

RSI_MAX = 68

RSI_OVERBOUGHT = 75

RSI_OVERSOLD = 30

# -----------------------------
# Volume Settings
# -----------------------------

RVOL_MIN = 1.2

RVOL_BREAKOUT = 1.5

RVOL_STRONG = 2.0

RVOL_EXTREME = 3.0

# -----------------------------
# Pullback Settings
# -----------------------------

PULLBACK_MIN = 3

PULLBACK_IDEAL = 6

PULLBACK_MAX = 12

# -----------------------------
# Risk Reward
# -----------------------------

MIN_RR = 2.0

GOOD_RR = 2.5

BEST_RR = 3.0

# -----------------------------
# ATR
# -----------------------------

ATR_MULTIPLIER = 2.0

# -----------------------------
# Scanner
# -----------------------------

LOOKBACK_SWING = 20

LOOKBACK_SR = 30

MIN_DATA = 200

# -----------------------------
# AI Score
# -----------------------------

BUY_SCORE = 80

STRONG_BUY_SCORE = 90

WATCH_SCORE = 70

# -----------------------------
# Trend
# -----------------------------

MIN_TREND_SCORE = 70

GOOD_TREND_SCORE = 90

BEST_TREND_SCORE = 120