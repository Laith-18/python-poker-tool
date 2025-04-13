# This code is part of a betting system for a game. It handles the user's bank balance and allows them to place bets.
class BettingSystem:
    def __init__(self,user_bank,visual_logic): # Constructor
        self.user_bank = user_bank
        self.current_bet = 0
        self.visual_logic = visual_logic

    def place_bet(self): # Method for placing a bet
        while True: # Loop until a valid bet is placed
            initial_bet = self.visual_logic.button_for_input_entry()
            initial_bet = str(initial_bet) # Convert the input to a string
            if initial_bet.isdigit(): # Validate the input
                initial_bet = int(initial_bet)
                if initial_bet > self.user_bank: # Check if the bet is greater than the user's bank
                    self.visual_logic.update_log("Bet exceeds your bank amount") # Outputs an error message
                    
                else:
                    var = self.update_bank_system(initial_bet) # Call the update_bank_system method
                    break # Exit the loop
            else:
                self.visual_logic.update_log("Invalid input. Please enter a valid bet amount.")
        return var
    
    def update_bank_system(self,initial_bet): # Method for updating the bank value
        self.user_bank = int(self.user_bank) -  int(initial_bet) # Update the bank value
        self.recent_bet = initial_bet # Set the recent bet to the initial bet
        return [self.user_bank, self.recent_bet] # Return the updated bank value and the bet
#Output format: [user_bank, recent_bet]
