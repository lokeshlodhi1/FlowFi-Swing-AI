import json

class Settings:

    def __init__(self):

        with open("config/strategy.json","r") as file:

            self.data=json.load(file)

    def get(self,key):

        return self.data.get(key)
