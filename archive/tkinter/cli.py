from login_system import LoginClass # Import LoginClass for user login and registration
from game_engine import GameEngine # Import GameEngine to handle the game logic
from strength_determiner import eval_hand # Import eval_hand to evaluate hand strength
import sys

class CommandLineGame:
    def __init__(self, master):

        self.login_system = LoginClass() # Create an instance of the LoginClass
        self.game_engine = GameEngine()
        print("Welcome to the Command Line Poker Game!")



    def login_loop(self):
        """Handles the login loop. It attempts to log in the user, and if successful, starts the game."""
        while True: # Loop until the user successfully logs in
            result = self.try_login() ## Call the try_login method to attempt login
            if result:
                break
            print("Login unsuccessful. Please try again.\n") # If login fails, prompt the user to try again
        username = result[1] # Get the username from the login method
        user_bank = result[2] # Get the user bank from the login method
        
        
        while True: # Loop to keep the game running until the user decides to exit
            self.play_game(username, user_bank) # Call the play_game method to start the game with the logged-in user's username and bank
            again = input("Do you want to play again? (yes/no): ") # Ask the user if they want to play again
            if again.lower() != "yes" and again.lower() != "y": # If the user does not want to play again, exit the loop and end the game
                break
        print("Thank you for playing! Goodbye!") # Print a goodbye message when the user decides to exit the game

    def try_login(self): # Method to handle the login process
        """Handles user login and starts the game if successful."""


        username = input("Enter your username: ").strip() # Get the username from the user input
        password = input("Enter your password: ").strip() # Get the password from the user input



        arr = self.login_system.login(username, password)  # Reused self.login_system


        if arr: # If the login is successful
            return [True,username,arr[1]] # Return the username and user bank
            # Output format: [condition, username, user_bank]




        else: # If the login fails
            print("Login failed. Please check your username and password.")
            yes_or_no = input("Would you like to register? (yes/no): ") # Ask if the user wants to register
            if yes_or_no.lower() == "yes" or yes_or_no.lower() == "y": # If the user wants to register
                outcome = self.login_system.register(username, password)  # Reused self.
                
                if outcome == "Registration successful": 
                    print("Registration successful!")
                    arr = self.login_system.login(username, password)  # Log in the user after successful registration
                    if arr:
                        return [True,username,arr[1]] # Return the username and user bank
                        # Output format: [condition, username, user_bank]
                else: 
                    print("Registration failed")
            else:
                print("Please try logging in again.")



    def action_recommendation(self,state): # Method to provide action recommendations based on the user's hand strength

        strength = eval_hand(state.user_deck, state.community_deck) # Evaluate the user's hand strength
        if strength > 5: # Check if the user's hand strength is greater than 5
            print("You have a strong hand, consider raising.")
        elif strength < 2: # Check if the user's hand strength is less than 2
            print("You have a weak hand, consider folding.")
        else: # Check if the user's hand strength is between 1 and 5
            print("You have a decent hand, consider calling.")
    

    def play_game(self,username, user_bank):

        state = self.game_engine.setup_new_game(username, user_bank) # Call the setup_new_game method to set up the initial game state


        #blinds
        state  = self.game_engine.determine_blinds(state)
        print(f"Small blind: {state.small_blind}, Pot: {state.pot}, User Bank: {state.user_bank}, Recent Bet: {state.recent_bet}, AI Bet: {state.ai_bet}") # Print the blinds and initial game state for testing purposes

        #tutorial mode
        decision = input("Do you want to enable tutorial mode? (yes/no): ") # Ask the user if they want to enable tutorial mode
        if decision.lower() == "yes": # If the user wants to enable tutorial mode
            state.tutorial_mode = True
        else:
            state.tutorial_mode = False
        
        #show hands
        print(f"Your hand: {state.user_deck}") # Show the user their hand
        print(f"AI's hand: {state.ai_deck}") # Show the user the AI's hand (for testing purposes, can be removed in production)

        if state.tutorial_mode:
            self.action_recommendation(state) # Call the action_recommendation method to give the user a recommendation based on their hand strength

        #preflop betting round
        outcome = self.game_engine.run_betting_round(state, user_goes_first=state.small_blind) # Call the run_betting_round method to handle the preflop betting round, passing in the game state and whether the user goes first based on the small blind
        if self.round_outcome(outcome, state):
            return # If the round outcome indicates the game is over, return to end the game
        
        #flop
        state.community_deck = self.game_engine.community_cards(state.community_deck, count=3) # Call the community_cards method to create the community cards for the flop
        print(f"Community cards: {state.community_deck}") # Show the user the community cards
        state = self.game_engine.evaluate_ai_strength(state) # Call the evaluate_ai_strength method to evaluate the AI's hand strength after the flop
        if state.tutorial_mode:
            self.action_recommendation(state) # Call the action_recommendation method to give the user a recommendation based on their hand strength after the flop

        outcome = self.game_engine.run_betting_round(state, user_goes_first=state.small_blind) # Call the run_betting_round method to handle the betting round after the flop, passing in the game state and whether the user goes first based on the small blind
        if self.round_outcome(outcome, state):
            return # If the round outcome indicates the game is over, return to end the game
        
        #turn
        state.community_deck = self.game_engine.community_cards(state.community_deck, count=1) # Call the community_cards method to add the turn card to the community deck
        print(f"Community cards: {state.community_deck}") # Show the user the community cards after the turn
        state = self.game_engine.evaluate_ai_strength(state) # Call the evaluate_ai_strength method to evaluate the AI's hand strength after the turn
        if state.tutorial_mode:
            self.action_recommendation(state) # Call the action_recommendation method to give the user a recommendation based on their hand strength after the turn

        outcome = self.game_engine.run_betting_round(state, user_goes_first=state.small_blind) # Call the run_betting_round method to handle the betting round after the turn, passing in the game state and whether the user goes first based on the small blind
        if self.round_outcome(outcome, state):
            return # If the round outcome indicates the game is over, return to end the game
        
        #river
        state.community_deck = self.game_engine.community_cards(state.community_deck, count=1) # Call the community_cards method to add the river card to the community deck
        print(f"Community cards: {state.community_deck}") # Show the user the community cards after the river
        state = self.game_engine.evaluate_ai_strength(state) # Call the evaluate_ai_strength method to evaluate the AI's hand strength after the river
        state.user_hand_strength = eval_hand(state.user_deck, state.community_deck) # Evaluate the user's hand strength after the river
        if state.tutorial_mode:
            self.action_recommendation(state) # Call the action_recommendation method to give the user a recommendation based on their hand strength after the river    

        #showdown
        self.show_result(state) # Call the show_result method to determine and display the result of the game after the showdown

    def round_outcome(self, outcome, state):
        if outcome == "fold": # If the user folds, the AI wins the pot
            print(f"You folded. AI wins the pot of ${state.pot}.") # Inform the user that they folded and the AI wins the pot
            return True # Return True to indicate the game is over
        elif outcome == "ai_fold": # If the AI folds, the user wins the pot
            print(f"AI folded. You win the pot of ${state.pot}!")
            return True # Return True to indicate the game is over
        elif outcome == False: # If the user goes all-in and loses, the AI wins the pot
            print(f"You went all-in and lost. AI wins the pot of ${state.pot}.")
            return True # Return True to indicate the game is over
        else:
            return False # Return False to indicate the game should continue
        
    def show_result(self, state):
        user_strength = eval_hand(state.user_deck, state.community_deck) # Evaluate the user's hand strength for the showdown
        ai_strength = eval_hand(state.ai_deck, state.community_deck) # Evaluate the AI's hand strength for the showdown

        print(f"\n--- Showdown ---")
        print(f"Your hand: {state.user_deck} | Strength: {user_strength}")
        print(f"AI's hand: {state.ai_deck} | Strength: {ai_strength}")
        print(f"Community: {state.community_deck}")

        result = self.game_engine.determine_result(state) # Call the determine_result method to determine the result of the showdown based on hand strengths
        if result == "win":
            print(f"You win the pot of ${state.pot}!")
        elif result == "lose":
            print(f"You lose. AI wins the pot of ${state.pot}.")
        else:
            print("It's a tie! Pot is split.")
        print(f"Your bank is now: ${state.user_bank}")