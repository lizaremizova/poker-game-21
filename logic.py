import random

class Game21:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        """game reset, starting again."""
        self.player_hand = []
        self.bot_hand = []
        self.game_over = False
        self.winner = None

    def deal_card(self):
        """returning random cards."""
        return random.randint(1, 11)

    def calculate_hand(self, hand):
        """counting score on hand."""
        return sum(hand)

    def player_hit(self):
        """player takes a card."""
        if not self.game_over:
            card = self.deal_card()
            self.player_hand.append(card)
            if self.calculate_hand(self.player_hand) > 21:
                self.game_over = True
                self.winner = 'bot'
            return card

    def player_stand(self):
        """bot takes turn."""
        self.bot_turn()

    def bot_turn(self):
        """bot's turn. Bot takes cards to 17 or more"""
        while not self.game_over and self.calculate_hand(self.bot_hand) < 17:
            card = self.deal_card()
            self.bot_hand.append(card)

        player_score = self.calculate_hand(self.player_hand)
        bot_score = self.calculate_hand(self.bot_hand)

        if bot_score > 21 or player_score > bot_score:
            self.winner = 'player'
        elif player_score < bot_score <= 21:
            self.winner = 'bot'
        else:
            self.winner = 'draw'

        self.game_over = True

    def get_game_state(self):
        """shows game current state."""
        return {
            'player_hand': self.player_hand,
            'player_score': self.calculate_hand(self.player_hand),
            'bot_hand': self.bot_hand if self.game_over else [],
            'bot_score': self.calculate_hand(self.bot_hand) if self.game_over else None,
            'game_over': self.game_over,
            'winner': self.winner
        }