class MessageFormatter:

    @staticmethod
    def format(trade):

        reasons = "\n".join([f"✅ {r}" for r in trade.reasons])

        return f"""
🚀 *FLOWFI AI ALERT*

🟢 *{trade.signal}*

📊 Stock : *{trade.symbol}*

🎯 Entry : ₹{trade.entry}

🛑 Stop Loss : ₹{trade.stop_loss}

🎯 Target 1 : ₹{trade.target1}

🎯 Target 2 : ₹{trade.target2}

📦 Quantity : {trade.quantity}

⭐ Confidence : {trade.confidence}%

📈 RR : {trade.risk_reward}

{reasons}
"""
