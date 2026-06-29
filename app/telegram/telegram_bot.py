import requests


class TelegramBot:

    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id

    def send_message(self, message: str):

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        payload = {

            "chat_id": self.chat_id,

            "text": message,

            "parse_mode": "Markdown"

        }

        response = requests.post(url, json=payload)

        return response.json()
