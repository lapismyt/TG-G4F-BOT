from msgspec import Struct
from msgspec.json import decode, encode

class UserSettings(Struct):
    conversation: list = []
    scenario: str = "default"
    model: str = "gpt-4-0613"

class User(Struct):
    id: str | int
    settings: UserSettings

class Data(Struct):
    users: list[User]

    def get_user(self, id):
        for usr in self.users:
            if usr.id == id:
                return usr
        return None

    def dump(self):
         with open("data.json", "w") as f:
            f.write(encode(self))
    
    @staticmethod
    def load():
        with open("data.json", "r") as f:
            data = decode(f.read(), type=Data)
        return data
