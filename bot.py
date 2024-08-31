from config import TOKEN
import telebot

bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect(DATABASE, check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    score INTEGER DEFAULT 0
)
''')
conn.commit()


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
# 
    bot.reply_to(message, """\
Hi there, I am 21Game bot.
I am here to play famous card game - 21\
""")


bot.infinity_polling()