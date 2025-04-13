# Description: This file contains the class BettingRounds which is responsible for the betting rounds in the game. 
# It contains the methods ai_first and user_first which are responsible for the betting rounds when the AI goes first and when the user goes first respectively.
# It also contains the method user_decision which is responsible for the user's decision making during the betting rounds. 
# The method decision_making is responsible for the AI's decision making during the betting rounds.

# ASCII flowchart showing the ai_first and user_first methods
# +------------------+------------------+
# |   ai_first       |   user_first     | 
# +------------------+------------------+
# |                  |                  |
# | 1. AI acts first  | 1. User acts first|
# |                  |                  |
# | 2. AI decision    | 2. User decision  |
# |                  |                  |
# | 3. User decision   | 3. AI decision    |
# |                  |                  |
# |                  |                  |
# | 4. Repeat until   | 4. Repeat until   |
# |    both players   |    both players   |
# |    check or fold  |    check or fold  |
# |                  |                  |
# |                  |                  |
# +------------------+------------------+
# |                  |                  |
# | 5. Return pot,    | 5. Return pot,    |
# |    user bank,     |    user bank,     |
# |    and recent bet |    and recent bet |
# |                  |                  |
# +------------------+------------------+

from user_decision_making import UserDecisionMaking
from ai_decision_making import PokerAI
import random

class BettingRounds:
    def __init__(self, ai_strength, pot, user_bank, recent_bet, visual_logic):
        self.ai_strength = ai_strength
        self.pot = pot
        self.user_bank = user_bank
        self.recent_bet = recent_bet
        self.visual_logic = visual_logic

    def ai_first(self):
        raise_amount = 1
        raise_amount_u = 0
        self.visual_logic.update_log("The AI acts first")
        while raise_amount != 0 or raise_amount_u != 0:
            temp = self.decision_making(True, raise_amount_u)
            if temp[0] == "call":
                self.visual_logic.update_log("The AI has called, matching the bet of: " + str(self.recent_bet))
                self.pot += self.recent_bet
                self.visual_logic.update_log(f"The pot is now: {self.pot}")
                self.visual_logic.update_pot(pot=self.pot)
                raise_amount = 0
            elif temp[0] == "raise":
                raise_amount = int(round(temp[1]))
                self.visual_logic.update_log(f"The AI has raised by: {raise_amount}")
                self.visual_logic.update_pot(pot=self.pot)
                self.pot += raise_amount
                self.recent_bet = raise_amount
                self.visual_logic.update_log(f"The pot is now: {self.pot}")
                self.visual_logic.update_pot(pot=self.pot)
            elif temp[0] == "fold":
                self.visual_logic.update_log("The AI has folded. Game over!")
                self.user_bank += self.pot
                self.visual_logic.update_user_bank(user_bank=self.user_bank)
                return False

            temp_u = self.user_decision(going_first=False, recent_bet=self.recent_bet)
            if temp_u == "fold":
                return "fold"
            elif isinstance(temp_u, list):
                raise_amount_u = int(temp_u[0])
                self.pot += raise_amount_u
                self.visual_logic.update_pot(pot=self.pot)
                self.user_bank = temp_u[2]
                self.recent_bet = temp_u[3]
                self.visual_logic.update_user_bank(user_bank=self.user_bank)
            if raise_amount == 0 and raise_amount_u == 0:
                break
        return [self.pot, self.user_bank, self.recent_bet]  # Return the pot and user bank after the betting round

    def user_first(self):
        raise_amount = 1
        raise_amount_u = 0
        self.visual_logic.update_log("You act first. Choose an action: Call, Raise, or Fold.")
        while raise_amount != 0:
            temp_u = self.user_decision(going_first=True,recent_bet=self.recent_bet)                
            if temp_u == "fold":
                return "fold"
    
            elif isinstance(temp_u, list):
                raise_amount_u = int(temp_u[0])  
                self.pot += raise_amount_u  # Add the user's raise amount to the pot
                #update pot on screen
                self.visual_logic.update_pot(pot=self.pot)
                self.user_bank = temp_u[2]
                self.visual_logic.update_user_bank(user_bank=self.user_bank)
                self.recent_bet = temp_u[3]
          
            temp = self.decision_making(False,raise_amount_u)
            if temp[0] == "fold":
                self.visual_logic.update_log("The AI has folded. Game over!")
                self.user_bank += self.pot  # Add the pot to the user's bank if AI folds
                self.visual_logic.update_user_bank(user_bank=self.user_bank)
                return "ai_folded"
            
            elif temp[0] == "call":
                self.visual_logic.update_log("The AI has called, matching your bet of: " + str(self.recent_bet))
                self.pot += self.recent_bet  # Add the recent bet to the pot
                self.visual_logic.update_log(f"The pot is now: {self.pot}")
                self.visual_logic.update_pot(pot=self.pot)
                raise_amount = 0
            
            elif temp[0] == "raise":
                raise_amount = int(round(temp[1]))
                self.visual_logic.update_log(f"The AI has raised by: {raise_amount}")
                self.pot += raise_amount + self.recent_bet  # Add both the raise amount and the recent bet to the pot
                self.visual_logic.update_pot(pot=self.pot)
                self.recent_bet = raise_amount + self.recent_bet  # Update the recent bet
                self.visual_logic.update_log(f"The pot is now: {self.pot}")
                self.visual_logic.update_pot(pot=self.pot)            
            if raise_amount == 0 and raise_amount_u == 0:
                break
            else:
                raise_amount = 1
        return [self.pot, self.user_bank, self.recent_bet]  # Return the pot and user bank after the betting round

    def user_decision(self, going_first,recent_bet):
        user_decision_maker = UserDecisionMaking(going_first, pot=self.pot, user_bank=self.user_bank, recent_bet=recent_bet, visual_logic=self.visual_logic)
        var = user_decision_maker.get_decision()
        if var == "fold":
            return("fold")
        else:
            return(var)

    def decision_making(self, going_first, raise_amount):
        poker_ai = PokerAI(going_first, strength=self.ai_strength, raise_amount= raise_amount, random_factor = random.random(), visual_logic=self.visual_logic)
        var = poker_ai.make_decision()
        return var