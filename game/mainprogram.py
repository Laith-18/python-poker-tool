# This is the main program for a poker game. It initializes the game, handles user input, and manages the game flow.
# It uses various classes and functions to handle different aspects of the game, such as card selection, betting rounds, and result determination.
# The program is designed to be modular and reusable
# The game is ran from this file, which imports the necessary classes and functions from other files.
# The game is designed to be played between a user and an AI opponent.
# The user can register, login, and manage their bank balance.
# The AI opponent makes decisions based on its strength and the current state of the game.
# The game includes various betting rounds, community cards, and a final result determination.
# The program uses the tkinter library for the graphical user interface.
# It follows this structure:
    # Step 1: Deal starting hands
    # Step 2: Determine blinds
    # Step 3: Begin betting rounds
    # Step 4: Deal community cards
    # Step 5: Evaluate hand strength
    # Step 6: Determine result
    # Step 7: Update user bank balance
    # Step 8: Save user data to JSON file
    # Step 9: Reset deck for next game
    # Step 10: End game


from card_selector import Deck # Import Deck class for card selection
from login_system import LoginClass # Import LoginClass for user login and registration
from blind_determiner import BlindDecider # Import BlindDecider class for blind determination
from strength_determiner import eval_hand # Import eval_hand function for hand evaluation
from result import ResultDeterminer # Import ResultDeterminer class for result determination
from betting_rounds import BettingRounds # Import BettingRounds class for betting rounds
from cli import CommandLineGame # Import CommandLineGame class for command


card_deck = Deck() # Create an instance of the Deck class
LoginClass().load_file() # Load user data from JSON file

def blind_decider(user_bank, pot, visual_logic): # Method to decide the blind
    blind_decider = BlindDecider(user_bank, pot, visual_logic) # Create an instance of the BlindDecider class
    game_state = blind_decider.decide_blind() # Call the decide_blind method
    return game_state
    # Output format: [pot, ai_bet, recent_bet, small_blind]

def handle_small_blind_user(user_bank, pot, visual_logic): # Method for the user small blind and the AI big blind logic
    blind_decider = BlindDecider(user_bank, pot, visual_logic) # Create an instance of the BlindDecider class
    game_state = blind_decider.small_blind_user() ## Call the small_blind_user method
    return game_state 
    # Output format: [pot, ai_bet, recent_bet, small_blind, user_bank]

def handle_small_blind_ai(user_bank, pot, visual_logic): # Method for the AI small blind and the user big blind logic
    blind_decider = BlindDecider(user_bank, pot, visual_logic) # Create an instance of the BlindDecider class
    game_state = blind_decider.ai_small_blind() # Call the ai_small_blind method
    return game_state

def card_selector(): # Method to select a card from the deck
    try: ## Try to select a card from the deck
        selected_card = card_deck.select_card() # Call the select_card method
        return ([selected_card[0],selected_card[1]]) ## Return the selected card
    except ValueError: # If the deck is empty, raise an error
        print("All cards have been used") 
    
def result_function(user_deck,ai_deck,community_deck,pot,username,user_bank,visual_logic): # Method to determine the result of the game
    result = ResultDeterminer(user_deck,ai_deck,community_deck,pot,username,user_bank,visual_logic) # Create an instance of the ResultDeterminer class
    result.determine_winner(pot) # Call the determine_winner method

def betting_round_ai_first(ai_strength, pot, user_bank, recent_bet, visual_logic): # Method for the AI first betting round
    betting_round = BettingRounds(ai_strength, pot, user_bank, recent_bet, visual_logic) ## Create an instance of the BettingRounds class
    game_state = betting_round.ai_first() # Call the ai_first method
    return game_state
    # Output format: [pot, user_bank, recent_bet]

def betting_round_user_first(ai_strength, pot, user_bank, recent_bet, visual_logic): # Method for the user first betting round
    betting_round = BettingRounds(ai_strength, pot, user_bank, recent_bet, visual_logic) # Create an instance of the BettingRounds class
    game_state = betting_round.user_first() # Call the user_first method
    return game_state
    # Output format: [pot, user_bank, recent_bet]

def starting_deck(): # Method to create the starting deck for the user and AI
    arr = [] # Create an empty array to store the starting deck
    for i in range(2): # Loop to select 2 cards for the starting deck
        arr.append(card_selector()) # Call the card_selector method to select a card
    return arr
    #Output: [[value, suit], [value, suit]]

def reset_deck(): # Method to reset the deck
    card_deck.reset_deck() # Call the reset_deck method of the Deck class

def community_cards(community_deck,x): # Method to create the community cards
    for i in range(x): # Loop to select x community cards
        card = card_selector() # Call the card_selector method to select a card
        community_deck.append(card) # Append the selected card to the community deck
    return community_deck
    #Output: [[value, suit], [value, suit], [value, suit], [value, suit], [value, suit]], max 5 cards

def main_game(username,user_bank): # Main game function
    pot = 0 # Initialize the pot to 0
    user_deck = starting_deck() # Create the starting deck for the user by calling the starting_deck method
    ai_deck = starting_deck() # Create the starting deck for the AI, calling the starting_deck method again
    ai_strength = eval_hand(ai_deck,com_cards=[]) # Evaluate the hand strength of the AI by calling the eval_hand method
    game_state = [username,user_bank,pot,user_deck,ai_deck,ai_strength] # Create a variable to store the game state
    
    
    cli_game = CommandLineGame(None)
    cli_game.main_game_command_line(game_state)


if __name__ == "__main__":
    game = CommandLineGame(None)
    game.login_loop_command_line()