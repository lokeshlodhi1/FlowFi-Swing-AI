import requests


class TelegramBot:

    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id

    def send_message(self, message: str):

        try:
            # Identify the bot
            me = requests.get(
                f"https://api.telegram.org/bot{self.token}/getMe",
                timeout=20
            ).json()

            print("\n========== BOT INFO ==========")
            print(me)
            print("==============================")

            url = f"https://api.telegram.org/bot{self.token}/sendMessage"

            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }

            response = requests.post(
                url,
                json=payload,
                timeout=20
            )

            data = response.json()

            print("\n========== TELEGRAM RESPONSE ==========")
            print(data)
            print("=======================================\n")

            return data.get("ok", False)

        except Exception as e:
            print("Telegram Error:", e)
            return False
