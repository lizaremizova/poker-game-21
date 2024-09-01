
import telebot
from telebot import types
import sqlite3
from config import TOKEN, DATABASE
from logic import Game21

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

active_games = {}

@bot.message_handler(commands=['start'])
def start_game(message):
    user_id = message.from_user.id
    username = message.from_user.username

    bot.send_message(message.chat.id, "Welcome to the game 21! type /hit, to take a card or /stand, to stop. Type /help to see all available commands")
    
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
        conn.commit()
  
    game = Game21()
    active_games[user_id] = game

   

@bot.message_handler(commands=['hit'])
def player_hit(message):
    user_id = message.from_user.id

    if user_id in active_games:
        game = active_games[user_id]
        card = game.player_hit()
        game_state = game.get_game_state()

        response = f"you took: {card}\nYour cards: {game_state['player_hand']} (sum: {game_state['player_score']})"
        
        if game_state['game_over']:
            response += f"\nGame over! You {'won' if game_state['winner'] == 'player' else 'lost'}. Bot's score: {game_state['bot_score']}"
            update_score(user_id, game_state['winner'])
            del active_games[user_id]
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "You haven't started the game. type /start.")


@bot.message_handler(commands=['stand'])
def player_stand(message):
    user_id = message.from_user.id

    if user_id in active_games:
        game = active_games[user_id]
        game.player_stand()
        game_state = game.get_game_state()

        response = f"Your cards: {game_state['player_hand']} (sum: {game_state['player_score']})\n"
        response += f"Bot's cards: {game_state['bot_hand']} (sum: {game_state['bot_score']})\n"
        response += f"Game over! You {'won' if game_state['winner'] == 'player' else 'lost'}."

        update_score(user_id, game_state['winner'])
        del active_games[user_id]
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "You haven't started the game. type /start.")

def update_score(user_id, winner):
    """score reloading in database."""
    if winner == 'player':
        cursor.execute("UPDATE users SET score = score + 1 WHERE user_id=?", (user_id,))
    elif winner == 'bot':
        cursor.execute("UPDATE users SET score = score - 1 WHERE user_id=?", (user_id,))
    conn.commit()

@bot.message_handler(commands=['score'])
def show_score(message):
    user_id = message.from_user.id
    cursor.execute("SELECT score FROM users WHERE user_id=?", (user_id,))
    score = cursor.fetchone()

    if score:
        bot.send_message(message.chat.id, f"Your currents score: {score[0]}")
    else:
        bot.send_message(message.chat.id, "You haven't started the game. type /start.")

@bot.message_handler(commands=['help'])
def show_help(message):
    help_text = (
        "available commands:\n"
        "/start - start new game\n"
        "/hit - take card\n"
        "/stand - stop and let the bot take turn\n"
        "/score - show your current score\n"
        "/help - show available commands"
    )
    bot.send_message(message.chat.id, help_text)

bot.polling(none_stop=True)