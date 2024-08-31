from config import TOKEN
import telebot

bot = telebot.TeleBot(TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
# 
    bot.reply_to(message, """\
Hi there, I am 21Game bot.
I am here to play famous card game - 21\
""")


bot.infinity_polling()