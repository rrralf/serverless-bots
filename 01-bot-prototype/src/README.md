# Telegram messages handling

pyTelegramBotAPI processes messages using your handlers. Handlers are defined using decorators

## 1. Processing commands (from the channel menu)

```python
@bot.message_handler(commands=['start', 'continue'])
def start_message(message):
    # your code goes here
```

This structure forms a message handler that responds to the 'start' and 'continue' commmands.


## 2. Response to regular text messages

```python
@bot.message_handler(content_types='text')
def generic_message_handler(message):
    # your code goes here
    if message.text == "<some text>":
        bot.send_message(message.chat.id,"i'm here")

    ...
```

---
## 3. The main menu in response to the /start command 

```python
import telebot

BOT_TOKEN = "..."

bot = telebot.TeleBot(
    token=BOT_TOKEN,
    threaded=True)

bot.set_my_commands([
    telebot.types.BotCommand("/start", "main menu"),
    telebot.types.BotCommand("/help", "print usage"),
])
```

---
