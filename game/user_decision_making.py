class UserDecisionMaking:

    """
    Handles the user's betting decisions in a poker game round.
    
    Parameters:
        going_first (bool): Whether the user goes first in this round.
        pot (int): The current pot value.
        user_bank (int): The user's current bank value.
        recent_bet (int): The most recent bet made by the opponent.
        visual_logic (VisualLogic): Object to handle UI interactions and display.
    """

    def __init__(self, going_first, pot, user_bank, recent_bet,visual_logic): # Constructor
        self.going_first = going_first
        self.pot = pot
        self.user_bank = user_bank
        self.recent_bet = recent_bet
        self.visual_logic = visual_logic # Initialize the class with the given parameters
    
    def get_decision(self): # Method for getting the user's decision
        """
        Gets the user's betting decision through the UI.
        Returns:
            str or list: The user's decision and updated game state info.
        """
        print("Actions: fold, call, raise") # Print the available actions to the user
        decision = input("Enter your decision: ").strip().lower() # Get the user's decision input
        raise_amount = 0
        if decision == "fold":
                return "fold"
        elif decision == "call":
            if self.recent_bet <= self.user_bank: # Check if the user can call
                self.pot += self.recent_bet # Add the recent bet to the pot
                self.user_bank -= self.recent_bet # Update the user's bank
                self.recent_bet = 0
                return [0, self.pot, self.user_bank, self.recent_bet]
                #Output format: [0, pot, user_bank, recent_bet]
        elif decision == "raise": 
            raise_amount = self.raise_function(raise_amount) # Call the raise_function method
            return raise_amount
            # Output format: [raise_amount, pot, user_bank, recent_bet] 

    def raise_function(self,raise_amount): # Method for raising the bet
        while True: # Loop until a valid raise amount is entered
            try: # Try to get the raise amount from the user
                raise_amount = int(input("Enter the amount you want to raise by: "))
                if raise_amount > self.user_bank: # Check if the raise amount is greater than the user's bank
                    print("You cannot raise by more than your bank")
                    return "retry" 
                else: # If the raise amount is valid, update the game state
                    raise_amount = raise_amount + self.recent_bet # Add the raise amount to the recent bet
                    self.pot += raise_amount # Add the raise amount to the pot
                    self.user_bank -= raise_amount # Update the user's bank
                    self.recent_bet = raise_amount # Update the recent bet
                    return [raise_amount, self.pot, self.user_bank, self.recent_bet]
                    # Output format: [raise_amount, pot, user_bank, recent_bet]
            except ValueError:
                print("Invalid input, try again")

