#i wanna play the game strictly through the command line

from login_system import LoginClass # Import LoginClass for user login and registration
import sys

class CommandLineGame:
    def __init__(self, master):
        self.master = master
        self.username = ""
        self.user_bank = ""
        self.raise_amount = 0
        self.login_system = LoginClass() # Create an instance of the LoginClass
        self.community_deck = [] # Initialize the community deck

        print("Welcome to the Command Line Poker Game!")


    def login_loop_command_line(self):
        """Handles the login loop. It attempts to log in the user, and if successful, starts the game."""
        while True: # Loop until the user successfully logs in
            game_state = self.try_login() ## Call the try_login method to attempt login
            if game_state:
                break
            print("Login unsuccessful. Please try again.\n") # If login fails, prompt the user to try again
        username = game_state[1] # Get the username from the login method
        user_bank = game_state[2] # Get the user bank from the login method
        self.condition = game_state[0] # Get the condition from the login method
        if self.condition: # If the login is successful
            from mainprogram import main_game  # Import main_game function here
            main_game(username, user_bank)  # Pass the instance of VisualLogic to main_game in mainprogram.py to run the main game loop through the command line

    def try_login(self): # Method to handle the login process
        """Handles user login and starts the game if successful."""


        username = input("Enter your username: ").strip() # Get the username from the user input
        password = input("Enter your password: ").strip() # Get the password from the user input



        arr = self.login_system.login(username, password)  # Reused self.login_system


        if arr: # If the login is successful
            self.condition = True 
            return [self.condition,username,arr[1]] # Return the username and user bank
            # Output format: [condition, username, user_bank]
        else: # If the login fails
            print("Login failed. Please check your username and password.")
            yes_or_no = input("Would you like to register? (yes/no): ") # Ask if the user wants to register
            if yes_or_no.lower() == "yes": # If the user wants to register
                game_state = self.login_system.register(username, password)  # Reused self.login_system
                if game_state == "Registration successful": 
                    print("Registration successful!")
                    arr = self.login_system.login(username, password)  # Log in the user after successful registration
                    if arr:
                        self.condition = True 
                        return [self.condition,username,arr[1]] # Return the username and user bank
                        # Output format: [condition, username, user_bank]
                else: 
                    print("Registration failed")
            else:
                print("Please try logging in again.")



    def action_recommendation(self): # Method to provide action recommendations based on the user's hand strength
        from mainprogram import eval_hand # Import eval_hand function here
        self.user_hand_strength = eval_hand(hand1=self.user_deck, com_cards=self.community_deck) # Evaluate the user's hand strength
        if self.user_hand_strength > 5: # Check if the user's hand strength is greater than 5
            print("You have a strong hand, consider raising.")
        elif self.user_hand_strength < 1: # Check if the user's hand strength is less than 1
            print("You have a weak hand, consider folding.")
        else: # Check if the user's hand strength is between 1 and 5
            print("You have a decent hand, consider calling.")
    

    def main_game_command_line(self,game_state): # Method to run the main game loop through the command line
        """Runs the main game loop through the command line."""
        from mainprogram import blind_decider, handle_small_blind_ai, handle_small_blind_user,eval_hand,betting_round_ai_first,betting_round_user_first,community_cards,result_function # Import the functions here

        self.username = game_state[0]
        self.user_bank = game_state[1]
        self.pot = game_state[2]
        self.user_deck = game_state[3]
        self.ai_deck = game_state[4]
        self.ai_strength = game_state[5]

        #Determine blinds
        small_blind = blind_decider(self.user_bank, self.pot) # Call the blind_decider method to determine the blinds
        self.pot = small_blind[0] # Update the pot with the small blind
        self.ai_bet = small_blind[1] # Get the AI bet from the blind
        self.recent_bet = small_blind[2] # Get the recent bet from the blind
        small_blind = small_blind[3] # Get the small blind from the blind determiner

        if small_blind == True:
            game_state = handle_small_blind_user(self.user_bank, self.pot) # Call the handle_small_blind_user method for the user small blind logic
            self.pot = game_state[0] # Update the pot after the small blind logic
            self.ai_bet = int(self.recent_bet) *2
            self.recent_bet = self.ai_bet
            self.small_blind = game_state[3] # Update the small blind variable
            self.user_bank = game_state[4] # Update the user bank after the small blind logic
        else:
            game_state = handle_small_blind_ai(self.user_bank, self.pot) # Call the handle_small_blind_ai method for the AI small blind logic
            self.pot = game_state[0]
            self.ai_bet = game_state[1]
            self.recent_bet = game_state[2]
            self.small_blind = game_state[3]
            self.user_bank = game_state[4]

        #ask if user wants tutorial mode or not
        decision = input("Do you want to enable tutorial mode? (yes/no): ") # Ask the user if they want to enable tutorial mode
        if decision.lower() == "yes": # If the user wants to enable tutorial mode
            self.tutorial_mode = True
        else:
            self.tutorial_mode = False
        
        #Preflop
        print(f"Your hand: {self.user_deck}") # Show the user their hand
        print(f"AI's hand: {self.ai_deck}") # Show the user the AI's hand (for testing purposes, can be removed in production)


        if self.tutorial_mode:
            self.action_recommendation() # Call the action_recommendation method to give the user a recommendation based on their hand strength


        if small_blind == True:
            game_state = betting_round_user_first(self.ai_strength, self.pot, self.user_bank, self.recent_bet) # Pass the instance of VisualLogic to betting_round_user_first in mainprogram.py
        else:
            game_state = betting_round_ai_first(self.ai_strength, self.pot, self.user_bank, self.recent_bet) # Pass the instance of VisualLogic to betting_round_ai_first in mainprogram.py

        if game_state == "fold":
            print("You folded. Game over!")
            sys.exit(0) #temp exit, will be replaced with proper game reset logic
        elif game_state == "ai_folded":
            print("The AI folded. You win the pot of: " + str(self.pot))
            sys.exit(0) #temp exit, will be replaced with proper game reset logic

        #Redefine the game state variables
        self.pot = game_state[0]
        self.user_bank = game_state[1]
        self.recent_bet = game_state[2]
        
        self.community_deck = community_cards(community_deck=self.community_deck, x=3)

        print(f"Community cards: {self.community_deck}") # Show the user the community cards

        # Check if the tutorial mode is enabled, and if so call the action_recommendation method
        if self.tutorial_mode == True:
            self.action_recommendation()
        
        #second round of betting
        self.ai_strength = eval_hand(hand1=self.ai_deck, com_cards=self.community_deck)
        if small_blind == True:
            game_state = betting_round_user_first(self.ai_strength, self.pot, self.user_bank, self.recent_bet) # Pass the instance of VisualLogic to betting_round_user_first in mainprogram.py
        else:
            game_state = betting_round_ai_first(self.ai_strength, self.pot, self.user_bank, self.recent_bet) # Pass the instance of VisualLogic to betting_round_ai_first in mainprogram.py

        if game_state == "fold":
            print("You folded. Game over!")
            sys.exit(0) #temp exit, will be replaced with proper game reset logic
        elif game_state == "ai_folded":
            print("The AI folded. You win the pot of: " + str(self.pot))
            sys.exit(0) #temp exit, will be replaced with proper game reset logic
        
        self.pot = game_state[0]
        self.user_bank = game_state[1]
        self.recent_bet = game_state[2]

        #the turn is revealed
        self.community_deck = community_cards(community_deck=self.community_deck, x=1) # Call the community_cards method to add the turn card to the community deck

        self.ai_strength = eval_hand(hand1=self.ai_deck, com_cards=self.community_deck) # Re-evaluate the AI's hand strength after the turn card is revealed
        if small_blind == True:
            game_state = betting_round_user_first(self.ai_strength, self.pot, self.user_bank, self.recent_bet) # Pass the instance of VisualLogic to betting_round_user_first in mainprogram.py
        else:
            game_state = betting_round_ai_first(self.ai_strength, self.pot, self.user_bank, self.recent_bet) # Pass the instance of VisualLogic to betting_round_ai_first in mainprogram.py

        if game_state == "fold":
            print("You folded. Game over!")
            sys.exit(0) #temp exit, will be replaced with proper game reset logic
        elif game_state == "ai_folded":
            print("The AI folded. You win the pot of: " + str(self.pot))
            sys.exit(0) #temp exit, will be replaced with proper game reset logic
        
        
        #Redefine the game state variables
        self.pot = game_state[0]
        self.user_bank = game_state[1]
        self.recent_bet = game_state[2]

        #the river is revealed
        self.community_deck = community_cards(community_deck=self.community_deck, x=1) # Call the community_cards method to add the river card to the community deck
        
        self.user_hand_strength = eval_hand(hand1=self.user_deck, com_cards=self.community_deck) # Re-evaluate the user's hand strength after the river card is revealed
        if self.tutorial_mode == True:
            self.action_recommendation() # Call the action_recommendation method to give the user a recommendation based on their hand strength
        
        self.ai_strength = eval_hand(hand1=self.ai_deck, com_cards=self.community_deck) # Re-evaluate the AI's hand strength after the river card is revealed
        if small_blind == True:
            game_state = betting_round_user_first(self.ai_strength, self.pot, self.user_bank, self.recent_bet) # Pass the instance of VisualLogic to betting_round_user_first in mainprogram.py
        else:
            game_state = betting_round_ai_first(self.ai_strength, self.pot, self.user_bank, self.recent_bet) # Pass the instance of VisualLogic to betting_round_ai_first in mainprogram.py
        
        if game_state == "fold":
            print("You folded. Game over!")
            sys.exit(0) #temp exit, will be replaced with proper game reset logic
        elif game_state == "ai_folded":
            print("The AI folded. You win the pot of: " + str(self.pot))
            sys.exit(0) #temp exit, will be replaced with proper game reset logic
        
        self.pot = game_state[0]
        self.user_bank = game_state[1]
        self.recent_bet = game_state[2]

        # Show the final results of the game
        result = result_function(self.user_deck, self.ai_deck, self.community_deck, self.pot, self.username, self.user_bank)        
        print(f"Your hand: {self.user_deck}, Hand Strength: {self.user_hand_strength}") # Show the user their hand and hand strength
        print(f"AI's hand: {self.ai_deck}, Hand Strength: {self.ai_strength}") # Show the user the AI's hand and hand strength
        print(f"Community cards: {self.community_deck}") # Show the user the community cards
        print(f"Result: {result}") # Show the user the result of the game
        if result == "win":
            print(f"You win the pot of: {self.pot}")
        elif result == "lose":
            print(f"The AI wins the pot of: {self.pot}")
        else:
            print("It's a tie! The pot is split.")

        