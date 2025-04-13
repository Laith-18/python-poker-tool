import random
class PokerAI: # Class for the AI decision making
    def __init__(self,going_first,strength,raise_amount,random_factor, visual_logic): # Constructor
        self.going_first = going_first
        self.strength = strength
        self.raise_amount = raise_amount
        self.random_factor = random_factor
        self.visual_logic = visual_logic

    def calculate_raise(self): # Method to calculate the raise amount
        min_raise = max(self.raise_amount *2, 10)  # Minimum raise is double the current raise or 10
        max_raise = self.raise_amount * (2 + self.strength / 3) # Maximum raise is double the current raise or 10
        return round(random.uniform(min_raise, max_raise)) # Return a random value between the min and max raise
        #Output: raise_amount

    def make_decision(self): # Method to make the decision
        # Bluff factor — AI bluffs more with weaker hands
        bluff_chance = max(0.1, (9 - self.strength) * 0.1) # Bluff chance is higher with weaker hands
        #0.1 has been chosen as the minimum bluff chance to avoid 0% bluffing

        if self.going_first == True: # If the AI is going first
            return self.small_blind_logic(bluff_chance) # Call the small_blind_logic method
        else:
            #self.visual_logic.update_log("AI is moving second, as its the big blind")
            return self.big_blind_logic(bluff_chance) # Call the big_blind_logic method

    def small_blind_logic(self,bluff_chance): # Method for the small blind logic
        
        # Small blind logic (first to act)
        if self.strength >= 7: # Strong hands
            return ("raise",self.calculate_raise()) if self.random_factor > 0.3 else ('call',None)  # 70% raise, 30% call
        elif 4 <= self.strength < 7: # Medium strength hands
            return 'call' if self.raise_amount <= 20 or self.random_factor > 0.4 else ('fold',None) # Calling if raise is low
        else: # Weak hands
            return("raise",self.calculate_raise()) if self.random_factor > bluff_chance else ('call',None) # Bluffing with weaker hands
            
    def big_blind_logic(self,bluff_chance): # Method for the big blind logic
        # Big blind logic (acting second)
            if self.strength >= 7: # Strong hands
                if self.raise_amount == 0: # No raise yet
                    return("raise",self.calculate_raise()) if self.random_factor > 0.3 else ('call',None) # Attacking limpers
                else: # Raising if raise is low
                    return("raise",self.calculate_raise()) if self.raise_amount < 50 and self.random_factor > 0.3 else ('call',None) # Reraising if raise is low
            elif 4 <= self.strength < 7: # Medium strength hands
                if self.raise_amount == 0: # No raise yet
                    return ('call',None)  # Checking if no raise
                else: # Raising if raise is low
                    return ('call',None) if self.raise_amount <= 30 or self.random_factor > 0.5 else ('fold',None) # Folding if raise is high
            else: # Weak hands
                if self.raise_amount == 0: # No raise yet
                    return ("raise",self.calculate_raise()) if self.random_factor < bluff_chance else ('call',None) # Bluffing with weaker hands
                else: # Raising if raise is low
                    return ('call',None) if self.random_factor < bluff_chance else ('fold',None) # Bluffing with weaker hands
#Output format: (decision,raise_amount) or (decision,None) if no raise