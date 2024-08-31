# import sqlite3
# from config import DATABASE
import random

# class DB_Manager:
#     def __init__(self, database):
#         self.database = database
        
#     def create_tables(self):
#         conn = sqlite3.connect(self.database)
#         with conn:
#             conn.execute('''CREATE TABLE players(
#                             player_id INTEGER PRIMARY KEY,
#                             wins_id INTEGER,
#                         )''') 
#             conn.commit()

#     def __executemany(self, sql, data):
#         conn = sqlite3.connect(self.database)
#         with conn:
#             conn.executemany(sql, data)
#             conn.commit()

CARDS = [str(x) for x in range(2, 11)] + ["J", "Q", "K", "A"] * 4

def deal_card():
  return random.choice(CARDS)

def player_value(hand):
  total = 0
  aces = 0
  for card in hand:
    if card in ["J", "Q", "K"]:
      total += 10
    elif card == "A":
      aces += 1
      total += 11
    else:
      total += int(card)
  while aces > 0 and total > 21:
    total -= 10
    aces -= 1
  return total


  
# if player_score > 21 or (dealer_score <= 21 and dealer_score > player_score):
#     print(f"Dealer Wins! Dealer total: {dealer_score}, Your total: {player_score}")
# elif dealer_score > 21 or player_score > dealer_score:
#     print(f"You Win! Your total: {player_score}, Dealer total: {dealer_score}")
# else:
#     print("Tie")