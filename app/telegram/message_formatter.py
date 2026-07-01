from datetime import datetime
import uuid


class MessageFormatter:

    def format(self, trade):

        trade_id = f"FLOWFI-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:4].upper()}"

        now = datetime.now()

        date = now.strftime("%d-%b-%Y")
        time = now.strftime("%I:%M %p")

        confidence_bar = "█" * int(trade.confidence / 10)
        confidence_bar += "░" * (10 - len(confidence_bar))

        reasons = ""

        for reason in trade.reasons:
            reasons += f"✅ {reason}\n"

        message = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 <b>FLOWFI AI SWING SCANNER</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟢 <b>{trade.signal}</b>

🏷 <b>Trade ID</b>
<code>{trade_id}</code>

🏢 <b>Stock</b>
<code>{trade.symbol}</code>

⏰ <b>Timeframe</b>
1 Day Swing

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 <b>Entry</b>
₹ {trade.entry:.2f}

🛑 <b>Stop Loss</b>
₹ {trade.stop_loss:.2f}

🎯 <b>Target 1</b>
₹ {trade.target1:.2f}

🎯 <b>Target 2</b>
₹ {trade.target2:.2f}

📦 <b>Quantity</b>
{trade.quantity}

⭐ <b>Confidence</b>
{confidence_bar}
{trade.confidence}%

📊 <b>Risk : Reward</b>
1 : {trade.risk_reward}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 <b>Trade Setup</b>

{reasons}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 <b>Date</b> : {date}
🕒 <b>Time</b> : {time}

⚠️ <i>Educational Purpose Only. Not Financial Advice.</i>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

        return message
