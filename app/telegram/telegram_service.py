from .telegram_bot import TelegramBot
from .message_formatter import MessageFormatter
from .duplicate_checker import DuplicateChecker


class TelegramService:

    def __init__(self, token, chat_id):

        self.bot = TelegramBot(token, chat_id)

        self.formatter = MessageFormatter()

        self.duplicate = DuplicateChecker()

    def send_trade(self, trade):

        if trade is None:
            return False

        # Send only high-confidence trades
        if trade.confidence < 75:
            return False

        if self.duplicate.already_sent(trade.symbol):
            return False

        message = self.formatter.format(trade)

        response = self.bot.send_message(message)

        self.duplicate.mark_sent(trade.symbol)

        return response
