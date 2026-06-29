import requests


class TelegramBot:

    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id

    def send_message(self, message: str):

        print("\n========== TELEGRAM CONFIG ==========")
        print("Token Exists :", bool(self.token))
        print("Chat ID      :", repr(self.chat_id))
        print("=====================================\n")

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }

        try:

            response = requests.post(
                url,
                json=payload,
                timeout=20
            )

            data = response.json()

            print("\n========== TELEGRAM RESPONSE ==========")
            print(data)
            print("=======================================\n")

            if data.get("ok") is True:
                return True

            return False

        except Exception as e:

            print("\n========== TELEGRAM ERROR ==========")
            print(str(e))
            print("====================================\n")

            return False
