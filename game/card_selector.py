# This script is part of a card game simulation. 
# It includes functions for managing the deck of cards, handling betting rounds, and determining the winner based on the cards held by the players. 
# The script also includes a class for managing the betting system and a class for handling user decisions during the game. 
# The code is designed to be modular and reusable, allowing for easy integration into a larger game framework.
import random
class Deck:
    def __init__(self): # Constructor
        self.suits = ["h", "d", "c", "s"] # h = hearts, d = diamonds, c = clubs, s = spades
        self.values =["2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "q", "k", "a"] # 2-10, j = jack, q = queen, k = king, a = ace
        self.deck = {f"{value} of {suit}": [value, suit] for suit in self.suits for value in self.values} # Create a dictionary of cards, in the format "value of suit": [value, suit]
        # Example: "2 of hearts": ["2", "h"]
        # The keys are the card names and the values are lists containing the value and suit
        # Output format: {card_name: [value, suit]}

    def select_card(self): # Method to select a card from the deck
        if not self.deck: # Check if the deck is empty
            raise ValueError("All cards have been used") 
        card = random.choice(list(self.deck.keys())) # Randomly select a card from the deck
        selected_card = self.deck.pop(card) # Remove the selected card from the deck
        return selected_card
        # Output format: [value, suit]
    
    def reset_deck(self): # Method to reset the deck
        self.deck = {f"{value} of {suit}": [value, suit] for suit in self.suits for value in self.values} # Create a new deck of cards
        