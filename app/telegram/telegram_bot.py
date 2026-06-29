import hashlib
import requests


class TelegramBot:

    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id

    def send_message(self, message: str):

        print("\n========== TELEGRAM CONFIG ==========")
        print("Token Exists :", bool(self.token))
        print("Chat Length  :", len(str(self.chat_id)))
        print("Chat Hash    :", hashlib.sha256(str(self.chat_id).encode()).hexdigest()[:12])
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

            return data.get("ok", False)

        except Exception as e:

            print("Telegram Error:", e)
            return False
