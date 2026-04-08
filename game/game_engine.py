from game.card_selector import Deck             
from game.login_system import LoginClass                 
from game.blind_determiner import BlindDecider            
from game.strength_determiner import eval_hand             
from game.result import ResultDeterminer                   
from game.betting_rounds import BettingRounds              
from game.game_state import GameState 


class GameEngine:
    def __init__(self):
        self.card_deck = Deck()
        self.login = LoginClass()
    
    def reset_deck(self): # Method to reset the deck
        self.card_deck.reset_deck() # Call the reset_deck method of the Deck class

    def card_selector(self): # Method to select a card from the deck
        try: # Try to select a card from the deck
            selected_card = self.card_deck.select_card() # Call the select_card method
            return ([selected_card[0],selected_card[1]]) # Return the selected card
        except ValueError: # If the deck is empty, raise an error
            print("All cards have been used") 
    
    def deal_hole_cards(self): # Method to create the starting deck for the user and AI
        return [self.card_selector(), self.card_selector()] # Call the card_selector method twice to select 2 cards for the starting deck
        #Output: [[value, suit], [value, suit]]
    
    def community_cards(self, community_deck, count): # Method to create the community cards
        for i in range(count): # Loop to select count community cards
            card = self.card_selector() # Call the card_selector method to select a card
            community_deck.append(card) # Append the selected card to the community deck
        return community_deck
        #Output: [[value, suit], [value, suit], [value, suit], [value, suit], [value, suit]], max 5 cards

    def determine_blinds(self, state):
        #combine the three blind functions into one function that takes in the state of the game and decides which blind function to call
        decider = BlindDecider(state.user_bank, state.pot)
        blind_result = decider.decide_blind()
        state.small_blind = blind_result[3]

        if state.small_blind:
            result = decider.small_blind_user()
            state.pot = result[0]
            state.recent_bet = result[2]
            state.ai_bet = state.recent_bet * 2
            state.recent_bet = state.ai_bet
            state.user_bank = result[4]
        else:
            result = decider.ai_small_blind()
            state.pot = result[0]
            state.recent_bet = result[2]
            state.ai_bet = result[1]
            state.user_bank = result[4] 
        
        return state

    def run_betting_round(self, state, user_goes_first, decision=None, raise_amount=0):

        betting = BettingRounds(state.ai_strength, state.pot, state.user_bank, state.recent_bet)

        if user_goes_first:
            result = betting.user_first(decision, user_raise_amount=raise_amount)
        else:
            result = betting.ai_first(decision, raise_amount=raise_amount)
        
        if result == "fold":
            return "fold"
        elif result == "ai_fold":
            state.user_bank += state.pot
            return "ai_fold"

        else:
            state.pot = result[0]
            state.user_bank = result[1]
            state.recent_bet = result[2]
            return result[3] # Return whether the round is over or should continue
        
    def evaluate_ai_strength(self, state):
        state.ai_strength = eval_hand(state.ai_deck, state.community_deck)
        return state

    def determine_result(self, state):
        result = ResultDeterminer(state.user_deck, state.ai_deck, state.community_deck, state.pot, state.username, state.user_bank, login_system=self.login_system)
        result = result.determine_winner(state.pot)

    def setup_new_game(self, username, user_bank):
        self.reset_deck()
        return GameState(
            username=username,
            user_bank=user_bank,
            pot=0,
            user_deck=self.deal_hole_cards(),
            ai_deck=self.deal_hole_cards(),
            ai_strength=0,
            community_deck=[],
        )