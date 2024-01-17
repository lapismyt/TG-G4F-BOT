from telebot import TeleBot
from telebot import types
import g4f
import models
import os
import time

with open("token.txt") as f:
    token = f.read().strip()

bot = TeleBot(token)

@bot.message_handler(commands=["copy"])
def copy(message):
    os.system(f"cp data.json copies/data-{int(time.time())}.json")
    with open("data.json", "rb") as f:
        file = f.read()
    bot.send_document(message.from_user.id, file, filename="data.json")
    bot.send_message(message.from_user.id, "Резервная копия создана.")

@bot.message_handler(commands=["start"])
def cmd_start(message):
    data = models.Data.load()
    if data.get_user(message.from_user.id) is None:
        user = models.User(message.from_user.id)
        data.users.append(user)
        data.dump()
    bot.send_message(message.from_user.id, "Привет! Если не знаешь, с чего начать - спроси меня о чём-нибудь. Ты можешь попросить меня рассказать исторический факт, написать код, или сочинить стихотворение.")

@bot.message_handler(commands=["clear"])
def clear_context(message):
    data = models.Data.load()
    user = data.get_user(message.from_user.id)
    user.settings.conversation = []
    data.dump()
    bot.send_message(message.from_user.id, "Переписка очищена.")

@bot.message_handler(content_types=["text"])
def text_handler(message):
    wait = bot.send_message(message.from_user.id, "Пожалуйста, подождите...")
    data = models.Data.load()
    user = data.get_user(message.from_user.id)
    user.settings.conversation.append({"role": "user", "content": message.text})
    response = g4f.ChatCompletion.create(
        model = g4f.models.gpt_4,
        messages = user.settings.conversation
    )
    user.settings.conversation.append({"role": "assistant", "content": response})
    data.dump()
    bot.send_message(message.from_user.id, response, parse_mode="markdown")
    bot.delete_message(wait.chat.id, wait.message_id)


if __name__ == "__main__":
    bot.infinity_polling()
