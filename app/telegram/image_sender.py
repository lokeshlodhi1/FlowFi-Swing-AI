import requests


class TelegramImageSender:

    def __init__(self, token, chat_id):

        self.token = token

        self.chat_id = chat_id

    def send(self, image_path, caption=""):

        url = f"https://api.telegram.org/bot{self.token}/sendPhoto"

        with open(image_path, "rb") as image:

            requests.post(

                url,

                data={

                    "chat_id": self.chat_id,

                    "caption": caption

                },

                files={

                    "photo": image

                }

            )
