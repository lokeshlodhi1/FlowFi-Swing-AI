TRADE_TABLE = """

CREATE TABLE IF NOT EXISTS trades(

id INTEGER PRIMARY KEY AUTOINCREMENT,

symbol TEXT,

signal TEXT,

entry REAL,

stop_loss REAL,

target1 REAL,

target2 REAL,

quantity INTEGER,

confidence REAL,

risk_reward REAL,

status TEXT,

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

"""

SIGNAL_TABLE = """

CREATE TABLE IF NOT EXISTS signals(

id INTEGER PRIMARY KEY AUTOINCREMENT,

symbol TEXT,

score REAL,

signal TEXT,

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

"""

JOURNAL_TABLE = """

CREATE TABLE IF NOT EXISTS journal(

id INTEGER PRIMARY KEY AUTOINCREMENT,

symbol TEXT,

entry REAL,

exit REAL,

pnl REAL,

holding_days INTEGER,

remarks TEXT,

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

"""
