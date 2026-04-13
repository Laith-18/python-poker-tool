from game.user_decision_making import UserDecisionMaking
from game.ai_decision_making import PokerAI
import random

class BettingRounds:
    def __init__(self, ai_strength, pot, user_bank, recent_bet):
        self.ai_strength = ai_strength
        self.pot = pot
        self.user_bank = user_bank
        self.recent_bet = recent_bet
        #self.visual_logic = visual_logic

    def ai_first(self, user_decision=None, user_raise_amount=0):

        if user_decision is None:
            temp = self.decision_making(True, 0)  # AI makes its initial decision with no raise amount
            if temp[0] == "call":
                self.pot += self.recent_bet
                return [self.pot, self.user_bank, 0, "round_over"]  # Return the pot and user bank after the betting round, along with a flag to indicate the round is over

            elif temp[0] == "raise":
                raise_amount = int(round(temp[1]))
                self.pot += raise_amount
                self.recent_bet = raise_amount
                return [self.pot, self.user_bank, self.recent_bet, "continue"]  # Return the pot and user bank after the betting round
            elif temp[0] == "fold":
                return "ai_folded"

        if user_decision:

            temp_u = self.user_decision(going_first=False, recent_bet=self.recent_bet, decision=user_decision, raise_amount=user_raise_amount)  # Get the user's decision based on the AI's action
            if temp_u == "fold":
                return "fold"
            elif isinstance(temp_u, list):
                raise_amount_u = int(temp_u[0])
                self.pot = temp_u[1]
                self.user_bank = temp_u[2]
                self.recent_bet = temp_u[3]
            
            if user_decision == "call":
                return [self.pot, self.user_bank, 0, "round_over"]  # Return the pot and user bank after the betting round, along with a flag to indicate the round is over

            temp = self.decision_making(True, raise_amount_u)
            if temp[0] == "fold":
                return "ai_folded"
            elif temp[0] == "call":
                self.pot += self.recent_bet  # Add the recent bet to the pot
                return [self.pot, self.user_bank, 0, "round_over"]  # Return the pot and user bank after the betting round, along with a flag to indicate the round is over
            elif temp[0] == "raise":
                raise_amount = int(round(temp[1]))
                self.pot += raise_amount  # Add the raise amount to the pot
                self.recent_bet = raise_amount  # Update the recent bet to the new raise amount
                return [self.pot, self.user_bank, self.recent_bet, "continue"]  # Return the pot and user bank after the betting round

    def user_first(self, user_decision, user_raise_amount):

        temp_u = self.user_decision(going_first=True,recent_bet=self.recent_bet,decision=user_decision, raise_amount=user_raise_amount)  # Get the user's decision based on the AI's action     
        if temp_u == "fold":
            return "fold"
    
        elif isinstance(temp_u, list):
            raise_amount_u = int(temp_u[0])  
            self.pot += raise_amount_u  
            self.user_bank = temp_u[2]
            self.recent_bet = temp_u[3]
        
        if user_decision == "call":
            return [self.pot, self.user_bank, 0, "round_over"] #lets flask know to move to the next phase after this betting round as user has called and there is no raise amount for the AI to respond to
          
        temp = self.decision_making(False,raise_amount_u)
        if temp[0] == "fold":
            return "ai_folded"

        elif temp[0] == "call":
                self.pot += self.recent_bet  # Add the recent bet to the pot
                return [self.pot, self.user_bank, 0, "round_over"]  # Return the pot and user bank after the betting round, along with a flag to indicate the round is over
            
        elif temp[0] == "raise":
            raise_amount = int(round(temp[1]))
            self.pot += raise_amount + self.recent_bet  # Add both the raise amount and the recent bet to the pot
            self.recent_bet = raise_amount + self.recent_bet  # Update the recent bet
            return [self.pot, self.user_bank, self.recent_bet, "continue"]  # Return the pot and user bank after the betting round

    def user_decision(self, going_first,recent_bet, decision, raise_amount):
        user_decision_maker = UserDecisionMaking(going_first, pot=self.pot, user_bank=self.user_bank, recent_bet=recent_bet)
        var = user_decision_maker.get_decision(decision, raise_amount)
        if var == "fold":
            return("fold")
        else:
            return(var)

    def decision_making(self, going_first, raise_amount):
        poker_ai = PokerAI(going_first, strength=self.ai_strength, raise_amount= raise_amount, random_factor = random.random())
        var = poker_ai.make_decision()
        return var