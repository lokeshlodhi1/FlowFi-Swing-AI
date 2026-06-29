TRADE_TABLE = """
CREATE TABLE IF NOT EXISTS trades (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    symbol TEXT NOT NULL,

    signal TEXT NOT NULL,

    confidence INTEGER,

    entry REAL,

    stop_loss REAL,

    target1 REAL,

    target2 REAL,

    quantity INTEGER,

    risk_reward REAL,

    reasons TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
"""

SIGNAL_TABLE = """
CREATE TABLE IF NOT EXISTS signals (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    symbol TEXT,

    score INTEGER,

    signal TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
"""

JOURNAL_TABLE = """
CREATE TABLE IF NOT EXISTS journal (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    symbol TEXT,

    entry REAL,

    exit REAL,

    pnl REAL,

    remarks TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
"""
