import os
import json
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("BOT_TOKEN environment variable undefined")
    exit(1)


bot = telebot.TeleBot(
    token=BOT_TOKEN,
    threaded=False )

# define main menu
bot.set_my_commands([
    telebot.types.BotCommand("/start", "main menu"),
    telebot.types.BotCommand("/hello_telebot", "say hello to Telebot :)"),
])


@bot.message_handler(commands=['start'])
def start_command_handler(message):
    username = message.chat.username

    bot.send_message(message.chat.id, f"Hi, {username}. It is start command handler")

@bot.message_handler(commands=['hello_telebot'])
def start_command_handler(message):
    username = message.chat.username

    bot.send_message(message.chat.id, f"Hi, {username}. It is hello_telebot handler!")

def handle_event(msg):
    json_string = json.dumps(msg)
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
