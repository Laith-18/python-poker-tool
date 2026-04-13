# This code is part of a betting system for a game. It handles the user's bank balance and allows them to place bets.
class BankSystem:
    def __init__(self,user_bank): # Constructor
        self.user_bank = int(user_bank)
        self.current_bet = 0
        self.recent_bet = 0

    def place_bet(self, entered_bet=None): # Method for placing a bet

        if entered_bet is None:
             return "No bet entered" # Output an error message if no bet is entered
        try:
            initial_bet = int(entered_bet) # Convert the entered bet to an integer
        except (TypeError, ValueError):
            return "invalid_bet" # Output an error message if the entered bet is not a valid integer
        if initial_bet <= 0:
            return "invalid_bet"
        if initial_bet > self.user_bank:
            return "invalid_funds"
        
        return self.update_bank_system(initial_bet) # Update the bank system with the initial bet and return the result
    
    def update_bank_system(self,initial_bet): # Method for updating the bank value
        self.user_bank = int(self.user_bank) -  int(initial_bet) # Update the bank value
        self.recent_bet = initial_bet # Set the recent bet to the initial bet
        return [self.user_bank, self.recent_bet] # Return the updated bank value and the bet
#Output format: [user_bank, recent_bet]
