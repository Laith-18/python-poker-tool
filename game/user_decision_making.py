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

    def __init__(self, going_first, pot, user_bank, recent_bet,): # Constructor
        self.going_first = going_first
        self.pot = pot
        self.user_bank = user_bank
        self.recent_bet = recent_bet
    
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

    def raise_function(self, raise_amount):
        while True:
            try:
                raise_amount = int(input("Enter the amount you want to raise by: "))
                if raise_amount <= 0:
                    print("Raise amount must be greater than 0.")
                    continue
                total_cost = raise_amount + self.recent_bet  # total chips user must put in
                if total_cost > self.user_bank:
                    print(f"You cannot afford that raise. You have {self.user_bank} chips.")
                    continue
                # Valid raise — update state
                self.user_bank -= total_cost
                self.pot += total_cost
                self.recent_bet = total_cost
                return [raise_amount, self.pot, self.user_bank, self.recent_bet]
            except ValueError:
                print("Invalid input, try again.")

