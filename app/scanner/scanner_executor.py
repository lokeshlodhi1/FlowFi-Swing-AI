from app.trade.trade_builder import TradeBuilder
from app.risk.risk_engine import RiskEngine

...

risk = RiskEngine(

    capital=100000,

    risk_percent=1

)

entry = float(last["Close"])

stop = float(last["EMA20"])

risk_result = risk.calculate(

    entry=entry,

    stop_loss=stop

)

trade = TradeBuilder().build(

    symbol=symbol,

    confidence=95,

    entry=entry,

    stop=stop,

    quantity=risk_result.quantity,

    reasons=[

        "EMA Pullback",

        "Trend Strong",

        "High Volume"

    ]

)

return trade
