from strength_determiner import eval_hand
from login_system import LoginClass
class ResultDeterminer:
    def __init__(self,user_deck,ai_deck,community_deck,pot,username,user_bank,login_system):
        self.user_deck = user_deck
        self.ai_deck = ai_deck
        self.community_deck = community_deck
        self.pot = pot
        self.username = username
        self.user_bank = user_bank
        self.login_system = login_system

    def evaluate_hands(self):
        p1 = eval_hand(self.user_deck,self.community_deck)
        p2 = eval_hand(self.ai_deck,self.community_deck)
        return p1,p2
    
    def display_hands(self):
        print("Your hand was: "+str(self.user_deck))
        print("The AI's hand was: "+str(self.ai_deck))
    
    def determine_winner(self,pot):
        self.pot = pot

        p1,p2 = self.evaluate_hands()
        self.display_hands()

        if p1 > p2:
            print("You have won")
            self.user_bank = self.user_bank + self.pot
            self.login_system.update_bank(self.username, self.user_bank)
            return "win"
        elif p1 < p2:
            print("You have lost")
            self.login_system.update_bank(self.username, self.user_bank)
            return "lose"
        else:
            print("It's a draw")
            self.user_bank = self.user_bank + self.pot/2
            self.login_system.update_bank(self.username, self.user_bank)
            return "draw"

    


