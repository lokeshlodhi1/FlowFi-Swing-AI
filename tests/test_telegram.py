from app.telegram.telegram_service import TelegramService
from app.trade.trade_signal import TradeSignal

trade = TradeSignal(

    symbol="BEL.NS",

    signal="BUY",

    confidence=96,

    entry=425.60,

    stop_loss=414.20,

    target1=448.40,

    target2=459.80,

    quantity=87,

    risk_reward=3,

    reasons=[

        "EMA Pullback",

        "Strong Trend",

        "High Volume"

    ]

)

service = TelegramService(

    token="YOUR_BOT_TOKEN",

    chat_id="YOUR_CHAT_ID"

)

service.send_trade(trade)
