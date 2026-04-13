import random
from game.bank_system import BankSystem

class BlindDecider:
    def __init__(self, user_bank, pot): # Constructor
        self.user_bank = user_bank
        self.pot = pot
        self.small_blind = None
        self.recent_bet = None
        self.ai_bet = None

    def decide_blind(self): # Method to decide the blind
        random_num = random.randint(0,1) # Picks either 0 or 1, and that utlises randomness to decide who is the small blind
        if random_num  == 0:
            self.small_blind = True # The user is the small blind
        else:
            self.small_blind = False # The user is not the small blind, hence the AI is the small blind
        self.ai_bet = 0
        self.recent_bet = 0
        return [self.pot, self.ai_bet, self.recent_bet, self.small_blind]
        #Output format: [pot, ai_bet, recent_bet, small_blind]

    def small_blind_user(self, entered_bet=None): # Method for the user small blind and the AI big blind logic
        bank_system = BankSystem(self.user_bank) # Create an instance of the BankSystem class
        result = bank_system.place_bet(entered_bet) # Call the place_bet method
        self.user_bank, self.recent_bet = result # Unpack the result
        big_blind = self.recent_bet * 2
        self.pot += self.recent_bet + big_blind # Add the recent bets to the pot
        game_state = [self.pot, self.ai_bet, self.recent_bet, self.small_blind, self.user_bank] # Return the game state
        return game_state
        #Output format: [pot, ai_bet, recent_bet, small_blind, user_bank]

    def ai_small_blind(self): # Method for the AI small blind and the user big blind logic
        self.ai_bet = random.randint(2,8) # Random small blind amount between 2 and 8, a fair and reasonable amount incase users are low on bank balance
        self.pot += self.ai_bet # Add the AI bet to the pot
        self.recent_bet = self.ai_bet*2 # The AI's bet is double the small blind
        self.user_bank -= self.recent_bet # Deduct the recent bet from the user's bank
        self.pot += self.recent_bet # Add the recent bet to the pot
        game_state = [self.pot, self.ai_bet, self.recent_bet, self.small_blind,self.user_bank] # Return the game state
        return game_state
        #Output format: [pot, ai_bet, recent_bet, small_blind, user_bank]
