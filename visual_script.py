# This script is part of a poker game simulation. It includes a class for managing the deck of cards, handling betting rounds, and determining the winner based on the cards held by the players. The script also includes a class for managing the betting system and a class for handling user decisions during the game. The code is designed to be modular and reusable, allowing for easy integration into a larger game framework.
# The script uses the tkinter library for the graphical user interface.
# Handles the GUI for login and poker gameplay using Tkinter.
# Manages user interaction, card visuals, betting buttons, and tutorial guidance.
# It follows this structure:
#     Step 1: Deal starting hands
#     Step 2: Determine blinds
#     Step 3: Begin betting rounds
#     Step 4: Deal community cards
#     Step 5: Evaluate hand strength
#     Step 6: Determine result
#     Step 7: Update user bank balance
#     Step 8: Save user data to JSON file
#     Step 9: Reset deck for next game
#     Step 10: End game

# ASCII flowchart showing the main game loop
# +------------------+------------------+
# |   Main Game Loop  |   End Game       |
# +------------------+------------------+
# |                  |                  |
# | 1. Deal starting  | 1. Save user data|
# |    hands         |    to JSON file  |
# |                  |                  |
# | 2. Determine blinds| 2. Reset deck   |
# |                  |                  |
# | 3. Begin betting  | 3. End game      |
# |    rounds        |                  |
# |                  |                  |
# | 4. Deal community |                  |
# |    cards         |                  |
# |                  |                  |
# | 5. Evaluate hand  |                  |
# |    strength      |                  |
# |                  |                  |
# | 6. Determine result|                  |
# |                  |                  |
# | 7. Update user    |                  |
# |    bank balance   |                  |
# |                  |                  |
# | 8. Ask to play    |                  |
# |    again         |                  |
# |                  |                  |
# | 9. End game       |                  |
# |                  |                  |
# +------------------+------------------+
# |                  |                  |
# | 10. Quit game    |                  |
# |                  |                  |
# +------------------+------------------+

import tkinter as tk # Import tkinter for GUI
import sys # Import sys for system exit
from tkinter import messagebox # Import messagebox for error messages
from login_system import LoginClass # Import LoginClass for user login and registration
from PIL import Image, ImageTk # Import Image and ImageTk for image handling

class VisualLogic: # Class for the visual logic of the game
    def __init__(self, master): ## Constructor
        self.master = master # Initialize the master window
        self.master.title("Poker Login") # Set the title of the window
        self.username = ""
        self.user_bank = ""
        self.raise_amount = 0
        self.var = tk.StringVar()  # Initialize var to None
        self.ready = tk.BooleanVar(value=False)  # Initialize ready as a BooleanVar
        self.login_system = LoginClass() # Create an instance of the LoginClass
        self.loaded_images = []  # Store references to prevent garbage collection
        self.community_deck = []  # Initialize community_deck as an empty list

        # Create the login form
        tk.Label(master, text="Username").grid(row=0, column=0, padx=10, pady=10) # Create a label for username
        self.username_entry = tk.Entry(master) # Create an entry for username
        self.username_entry.grid(row=0, column=1, padx=10, pady=10) # Create a grid for the entry

        # Create the password form
        tk.Label(master, text="Password").grid(row=1, column=0, padx=10, pady=10) # Create a label for password
        self.password_entry = tk.Entry(master, show="*") # Create an entry for password
        self.password_entry.grid(row=1, column=1, padx=10, pady=10) # Create a grid for the entry

        # Create the login button
        self.login_button = tk.Button(master, text="Login", command=self.login_loop) # Create a button for login
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10) # Create a grid for the button

    def button_for_input_entry(self): # Creates a button for input entry
        self.input_variable= tk.StringVar() # Initialize input_variable as a StringVar
        self.input_entry = tk.Entry(self.canvas) # Create an entry for input
        self.canvas.create_window((600, 850), window=self.input_entry, anchor="n")  # Centered at the top
        self.input_button = tk.Button(self.canvas, text="Submit", command=self.get_input_value) # Create a button for input
        self.canvas.create_window((700, 850), window=self.input_button, anchor="n") # Centered at the top
        self.master.wait_variable(self.input_variable)  # Wait for the input to be processed
        input_value = self.input_entry.get() # Get the input value
        self.input_entry.destroy() # Destroy the input entry
        self.input_button.destroy() # Destroy the input button
        return input_value # Return the input value

    def update_log(self, message): # Method to update the log box
        """Updates the log box with a new message."""
        self.log_box.insert(tk.END, message + "\n")
        self.master.update() # Update the log box with the new message
    
    def clear_log(self): # Method to clear the log box
        """Clears the log box."""
        self.log_box.delete(1.0, tk.END) # Clear the log box
        self.master.update() # Update the log box
    
    def clear_guide(self): # Method to clear the guide box
        """Clears the guide box."""
        self.guide_box.delete(1.0, tk.END) # Clear the guide box
        self.master.update() # Update the guide box
    

    def get_input_value(self):  # Method to get the input value from the entry
        """Handles the action when the user submits input."""
        input_value = self.input_entry.get() # Get the input value from the entry
        try: # Convert the input value to an integer
            self.input_value = int(input_value)
        except ValueError: # If the input value is not an integer, show an error message
            self.input_value = input_value
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            return
        if input_value.isdigit(): # Check if the input value is a digit
            self.condition = True # Set the condition to True
            self.input_variable.set(input_value)  # Set the variable to trigger wait_variable
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid number.") # Show an error message

    def login_loop(self): # Method to handle the login loop
        """Handles the login loop. It attempts to log in the user, and if successful, starts the game."""
        game_state = self.try_login() ## Call the try_login method to attempt login
        username = game_state[1] # Get the username from the login method
        user_bank = game_state[2] # Get the user bank from the login method
        self.condition = game_state[0] # Get the condition from the login method
        if self.condition: # If the login is successful
            from mainprogram import main_game  # Import main_game function here
            main_game(username, user_bank, self)  # Pass the instance of VisualLogic to main_game

    def tutorial_mode_enabled(self): # Method to handle the action when the user is ready to play
        """Handles the action when the user is ready to play."""
        self.tutorial_label.destroy() # Destroy the tutorial label
        self.yes_button.destroy() # Destroy the yes button
        self.no_button.destroy() # Destroy the no button
        self.log_box.delete(1.0, tk.END) # Clear the log box
        self.master.update() # Update the log box
        self.ready.set(True)  # Set the ready variable to True
        return True # Return True to indicate that the user is ready to play

    def tutorial_mode_disabled(self): # Method to handle the action when the user is not ready to play
        self.tutorial_label.destroy() # Destroy the tutorial label
        self.yes_button.destroy() # Destroy the yes button
        self.no_button.destroy() # Destroy the no button
        self.log_box.delete(1.0,tk.END) # Clear the log box
        self.master.update() # Update the log box
        self.ready.set(False) # Set the ready variable to False

    def try_login(self): # Method to handle the login process
        """Handles user login and starts the game if successful."""
        username = self.username_entry.get() # Get the username from the entry
        password = self.password_entry.get() # Get the password from the entry
        arr = self.login_system.login(username, password)  # Reused self.login_system
        if arr: # If the login is successful
            self.condition = True 
            return [self.condition,username,arr[1]] # Return the username and user bank
            # Output format: [condition, username, user_bank]
        else: # If the login fails
            messagebox.showinfo("Error", "Login failed")
            if messagebox.askyesno("Register", "Would you like to register?"): # Ask if the user wants to register
                game_state = self.login_system.register(username, password)  # Reused self.login_system
                if game_state == "Registration successful": 
                    messagebox.showinfo("Success", "Registration successful!") 
                else: 
                    messagebox.showerror("Error", "Registration failed")
                    self.username_entry.delete(0, tk.END) # Clear the username entry
                    self.password_entry.delete(0, tk.END) # Clear the password entry
            else:
                self.username_entry.delete(0, tk.END) # Clear the username entry
                self.password_entry.delete(0, tk.END) ## Clear the password entry
        
    def betting_buttons(self): # Method to handle the betting buttons
        self.log_box.insert(tk.END, "Choose an action: Call, Raise, or Fold.\n")
        self.var = tk.StringVar()  # Initialize var to None
        #get a string variable from a button press
        self.call_button = tk.Button(self.canvas, text="Call", command=lambda: self.var.set("call")) # Create a button for call
        self.canvas.create_window((550,850), window=self.call_button, anchor="s")  # Bottom middle corner
        self.raise_button = tk.Button(self.master, text="Raise", command=lambda: self.var.set("raise")) # Create a button for raise, next to the call button
        self.canvas.create_window((600,850), window=self.raise_button, anchor="s")  # Bottom middle corner
        self.fold_button = tk.Button(self.master, text="Fold", command=lambda: self.var.set("fold")) # Create a button for fold, next to the raise button
        self.canvas.create_window((650,850), window=self.fold_button, anchor="s")  # Bottom middle corner
        self.master.wait_variable(self.var)  # Get the decision from the variable
        decision = self.var.get()  # Get the decision from the variable
        decision = str(decision)  # Convert to string

        self.call_button.destroy() # Destroy the call button
        self.raise_button.destroy() # Destroy the raise button
        self.fold_button.destroy()  # Destroy the fold button
        self.master.update() # Update the canvas
        self.condition = True

        if decision == "raise": 
            while True:
                raise_amount = self.button_for_input_entry() # Call the button_for_input_entry method to get the raise amount
                if raise_amount == "":
                    messagebox.showerror("Invalid Input", "Please enter a valid number.")
                    continue
                break # Loop until a valid raise amount is entered
            try: 
                raise_amount = int(raise_amount)  # Convert to integer
            except:
                raise_amount = str(raise_amount)  # If it fails, set raise_amount to a string
            # if raise_amount is not an integer
            if not isinstance(raise_amount, int): # Check if raise_amount is an integer
                messagebox.showerror("This number is not an integer, your raise has been set to 1")
                raise_amount = 1 # Set raise_amount to 1 if it is not an integer, because validation is needed
            
            if raise_amount < 0 or raise_amount > self.user_bank: # Check if raise_amount is less than 0 or greater than user_bank
                messagebox.showerror("Error","Raise amount must be between 0 and your bank. You instead have folded")
                raise_amount = 0
                decision = "fold"
            self.raise_button.destroy() # Destroy the raise button
            self.master.update() # Update the canvas

        elif decision == "call":
            if self.recent_bet > self.user_bank: # Check if the recent bet is greater than user_bank
                messagebox.showerror("Error", "You cannot call, you have folded") # Validation is needed
                decision = "fold"
        return decision, self.raise_amount
        # Output format: [decision, raise_amount]

    def get_raise_amount(self): # Method to handle the action when the user wants to enter a raise amount
        """Handles the action when the user wants to enter a raise amount."""
        self.raise_amount = self.raise_amount.get() # Get the raise amount from the entry
        try:
            self.raise_amount = int(self.raise_amount)  # Convert to integer
            self.raise_amount_button.destroy() # Destroy the raise amount button
        except ValueError:
            self.raise_amount = str(self.raise_amount)
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            return

    def update_pot(self, pot): # Method to update the pot label and value
        """Updates the pot label and pot value"""
        self.pot_label.config(text=f"Pot: {pot}") # Update the pot label with the new value
        self.pot = pot # Update the pot value
        self.master.update() # Update the pot label with the new value
    
    def update_user_bank(self, user_bank): # Method to update the user bank label and value
        """Updates the user bank label and user bank value"""
        self.user_bank_label.config(text=f"Your Bank: {user_bank}") # Update the user bank label with the new value
        self.user_bank = user_bank # Update the user bank value
        self.master.update() # Update the user bank label with the new value
        

    def add_cards_to_deck(self,frame,img_path): # Method to add cards to the deck
        image_path = img_path # Get the image path from the argument
        image = Image.open(image_path) # Open the image using PIL
        image = image.resize((100, 150))  # Resize the image to 100x150 pixels
        image = ImageTk.PhotoImage(image) # Create a PhotoImage object from the image
        self.loaded_images.append(image) # Store the reference to prevent garbage collection
        label = tk.Label(frame, image=image) # Create a label to display the image
        label.pack(side="left", padx=5) # Pack the label to the left with some padding

    def action_recommendation(self): # Method to provide action recommendations based on the user's hand strength
        from mainprogram import eval_hand # Import eval_hand function here
        self.user_hand_strength = eval_hand(hand1=self.user_deck, com_cards=self.community_deck) # Evaluate the user's hand strength
        if self.user_hand_strength > 5: # Check if the user's hand strength is greater than 5
            self.guide_box.insert(tk.END, "You have a strong hand, consider raising.\n")
        elif self.user_hand_strength < 1: # Check if the user's hand strength is less than 1
            self.guide_box.insert(tk.END, "You have a weak hand, consider folding.\n")
        else: # Check if the user's hand strength is between 1 and 5
            self.guide_box.insert(tk.END, "You have a decent hand, consider calling.\n")

    def ask_to_play_again(self): # Method to ask the user if they want to play again
        self.play_again_label = tk.Label(self.canvas, text="Do you want to play again?") # Creates a label on the canvas asking if the user wants to play again
        self.canvas.create_window((1000, 700), window=self.play_again_label, anchor="n")  # Centered at the right
        self.play_again_button = tk.Button(self.canvas, text="Yes", command=self.play_again) # Creates a button on the canvas for the user to play again
        self.canvas.create_window((1000, 800), window=self.play_again_button, anchor="n")  # Centered at the right
        self.quit_button = tk.Button(self.canvas, text="No", command=self.quit_game) # Creates a button on the canvas for the user to quit the game
        self.canvas.create_window((1050, 800), window=self.quit_button, anchor="n")  # Centered at the right
        self.master.mainloop() # Run the main loop of the canvas

    def user_folded(self): # Method to handle the action when the user folds
        self.log_box.insert(tk.END, "You have folded. Game over!\n")
        self.master.update() # Update the log box with the new message
        self.update_user_bank(user_bank=self.user_bank) # Update the user bank label with the new value
        self.ask_to_play_again() # Ask the user if they want to play again
        return

    def ai_folded(self): # Method to handle the action when the AI folds
        self.log_box.insert(tk.END, "The AI has folded. You win!\n")
        self.master.update() # Update the log box with the new message
        self.user_bank += self.pot # Due to winning, add the pot to the user bank
        self.update_user_bank(user_bank=self.user_bank) # Update the user bank label with the new value
        self.ask_to_play_again() # Ask the user if they want to play again
        return

    def play_again(self): # Method to handle the action when the user wants to play again
        self.play_again_label.destroy() # Destroy the play again label
        self.play_again_button.destroy() # Destroy the play again button
        self.quit_button.destroy() # Destroy the quit button
        self.log_box.insert(tk.END, "You chose to play again!\n")
        self.master.update() # Update the log box with the new message, and makes the play again button and label disappear
        self.community_deck = []  # Reset community_deck to an empty list
        self.user_deck = []  # Reset user_deck to an empty list
        self.ai_deck = []  # Reset ai_deck to an empty list
        self.pot = 0  # Reset pot to 0
        self.user_bank = 0  # Reset user_bank to 0
        self.ai_strength = 0  # Reset ai_strength to 0
        self.recent_bet = 0  # Reset recent_bet to 0
        # Variables are cleared to prevent logic errors in the next game
        from mainprogram import main_game, reset_deck # Import main_game and reset_deck functions here
        reset_deck()  # Reset the deck
        main_game(self.username, self.user_bank, self) # Pass the instance of VisualLogic to main_game as self
        # Call the main_game function to start a new game
    
    def quit_game(self): # Method to handle the action when the user wants to quit the game
        self.play_again_label.destroy() # Destroy the play again label
        self.play_again_button.destroy() # Destroy the play again button
        self.quit_button.destroy() # Destroy the quit button
        self.log_box.insert(tk.END, "Goodbye!\n") 
        self.master.update() # Update the log box with the new message, and makes the quit button and label disappear
        self.master.destroy() # Destroy the master window
        sys.exit(0) # Exit the program

    def main_game_visual(self,var): # Main method to create the main game window and handle the game logic
        """""Main method to create the main game window and handle the game logic."""
        
        from mainprogram import blind_decider, handle_small_blind_ai, handle_small_blind_user,eval_hand,betting_round_ai_first,betting_round_user_first,community_cards,result_function # Import the functions here
        game_window = tk.Toplevel(self.master) # Create a new window for the game
        game_window.title("Poker Game") # Set the title of the window
        game_window.geometry("1200x900") # Set the resolution of the window
        self.master = game_window  # Set the master to the new window
        self.username = var[0] # Get the username from the argument
        self.user_bank = var[1] # Get the user bank from the argument
        self.pot = var[2] # Get the pot from the argument
        self.user_deck = var[3] # Get the user deck from the argument
        self.ai_deck = var[4] # Get the AI deck from the argument
        self.ai_strength = var[5] # Get the AI strength from the argument

        #Create the main frame and background
        main_frame = tk.Frame(self.master) # Create a frame for the main window
        main_frame.pack(fill=tk.BOTH, expand=True) # Pack the frame to fill the window
        self.background_image = Image.open("cards/background.jpg") # Open the background image using PIL
        self.background_image = ImageTk.PhotoImage(self.background_image.resize((1200, 900))) # Resize the image to fit the window
        self.canvas = tk.Canvas(main_frame, width=self.background_image.width(), height=self.background_image.height()) # Create a canvas to display the background image
        self.canvas.pack(fill=tk.BOTH, expand=True) # Pack the canvas to fill the window
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_image) # Create an image on the canvas using the background image

        #Create log box
        self.log_box = tk.Text(self.canvas, height=4, width=100) # Create a text box for the log box
        self.canvas.create_window((600, 50), window=self.log_box, anchor="n")  # Centered at the top
        self.log_box.insert(tk.END, f"Welcome {self.username}!\n") # Insert a welcome message in the log box

        #Create a pot label to the left of the screen
        self.pot_label = tk.Label(self.canvas, text=f"Pot: {self.pot}") # Create a label for the pot
        self.canvas.create_window((50, 50), window=self.pot_label, anchor="nw")  # Top left corner

        #Create a user bank label to the left of the screen
        self.user_bank_label = tk.Label(self.canvas, text=f"Your Bank: {self.user_bank}") # Create a label for the user bank
        self.canvas.create_window((50, 100), window=self.user_bank_label, anchor="nw")  # Top left corner

        #Mapping for cards
        ranks = {'2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '10': '10', 'j': 'jack', 'q': 'queen', 'k': 'king', 'a': 'ace'}
        suits = {'c': 'clubs', 'd': 'diamonds', 'h': 'hearts', 's': 'spades'}

        #Decide who the small blind is
        small_blind = blind_decider(self.user_bank, self.pot, self)  # Pass the instance of VisualLogic to blind_decider
        self.pot = small_blind[0] # Update the pot value
        self.ai_bet = small_blind[1] # Update the AI bet value
        self.recent_bet = small_blind[2] ## Update the recent bet value
        small_blind = small_blind[3] ## Get the small blind value

        if small_blind == True: # If the user is the small blind
            game_state = handle_small_blind_user(self.user_bank, self.pot, self)  # Pass the instance of VisualLogic to handle_small_blind_user in mainprogram.py
            self.pot = game_state[0]
            self.recent_bet = game_state[2]
            self.ai_bet = self.recent_bet*2
            self.recent_bet = self.ai_bet
            self.small_blind = game_state[3]
            self.user_bank = game_state[4]
            #Output in log box the actions done
            self.log_box.insert(tk.END, f"You placed the small blind of {self.recent_bet}.\n")
            self.log_box.insert(tk.END, f"Your current balance is: {self.user_bank}\n")
            self.log_box.insert(tk.END, f"AI placed the big blind of {self.ai_bet}.\n")
            
        else:
            game_state = handle_small_blind_ai(self.user_bank, self.pot, self) # Pass the instance of VisualLogic to handle_small_blind_ai in mainprogram.py
            self.pot = game_state[0]
            self.ai_bet = game_state[1]
            self.recent_bet = game_state[2]
            self.small_blind = game_state[3]
            self.user_bank = game_state[4]
            #Output in log box the actions done
            self.log_box.insert(tk.END, f"AI placed the small blind of {self.ai_bet}.\n")
            self.log_box.insert(tk.END, f"You placed the big blind of {self.recent_bet}.\n")
            self.log_box.insert(tk.END, f"Your current balance is: {self.user_bank}\n")
        
        #Update the pot label and user bank label
        self.update_user_bank(user_bank=self.user_bank) # Update the user bank label with the new value

        #Ask the user if they want tutorial mode enabled
        self.tutorial_label = tk.Label(self.canvas, text="Would you like tutorial mode enabled?")
        self.canvas.create_window((600, 200), window=self.tutorial_label, anchor="n")  # Centered at the top
        self.yes_button = tk.Button(self.canvas, text="Yes", command=self.tutorial_mode_enabled) # Create a button for yes
        self.canvas.create_window((600, 300), window=self.yes_button, anchor="n")  # Centered at the top
        self.no_button = tk.Button(self.canvas, text="No", command=self.tutorial_mode_disabled) # Create a button for no
        self.canvas.create_window((600, 350), window=self.no_button, anchor="n")  # Centered at the top

        #Dont move on to the next step until the user is ready to play
        self.master.wait_variable(self.ready)  # Wait for the user to be ready
        if self.ready.get(): 
            #Create a guide box to the left of the screen
            self.tutorial_mode_on = True 
            self.guide_box = tk.Text(self.canvas, height=4, width=30) # Create a text box for the guide box
            self.canvas.create_window((50, 200), window=self.guide_box, anchor="nw")  # Top left corner
        else:
            self.tutorial_mode_on = False 
            
        #Create a frame for the user deck and ai deck and community deck
        self.ai_frame = tk.Frame(self.canvas) # Create a frame for the AI deck
        self.community_frame = tk.Frame(self.canvas) # Create a frame for the community deck
        self.user_frame = tk.Frame(self.canvas) # Create a frame for the user deck
        self.canvas.create_window((600, 800), window=self.user_frame, anchor="s") # Bottom middle of the window
        self.canvas.create_window((600, 400), window=self.community_frame, anchor="n") # Centered at the top, in the middle of the window
        self.canvas.create_window((900, 200), window=self.ai_frame, anchor="n") # Centered at the top, to the right of the window

        #Setting up cards
        for card in self.user_deck: #For each card in user_deck
            rank = card[0] #Get the rank of the card
            suit = card[1] #Get the suit of the card
            image_path = f"cards/{ranks[rank]}_of_{suits[suit]}.png" #Load the image
            self.add_cards_to_deck(frame=self.user_frame,img_path=image_path) #Call the add_cards_to_deck method to add the card to the user deck
            
        for card in self.ai_deck: #For each card in ai_deck
            image_path = f"cards/back.jpg" #Load the image
            self.add_cards_to_deck(frame=self.ai_frame,img_path=f"cards/back.jpg") #Call the add_cards_to_deck method to add the card to the AI deck

        for i in range(5): #For each card in the community deck
            image_path = f"cards/back.jpg" #Load the image
            self.add_cards_to_deck(frame=self.community_frame,img_path=image_path) #Call the add_cards_to_deck method to add the card to the community deck

        if self.tutorial_mode_on == True: # If tutorial mode is enabled
            self.action_recommendation() # Provide action recommendations based on the user's hand strength, by calling the action_recommendation method

        

        #First round of betting
        if small_blind == True: #If the user is the small blind
            game_state = betting_round_user_first(self.ai_strength, self.pot, self.user_bank, self.recent_bet, self) # Pass the instance of VisualLogic to betting_round_user_first in mainprogram.py
        else:
            game_state = betting_round_ai_first(self.ai_strength, self.pot, self.user_bank, self.recent_bet, self) # Pass the instance of VisualLogic to betting_round_ai_first in mainprogram.py

        if game_state == "fold": 
            self.user_folded() # If the user folds, call the user_folded method
        elif game_state == "ai_folded":
            self.ai_folded() # If the AI folds, call the ai_folded method

        #Redefine the game state variables
        self.pot = game_state[0]
        self.user_bank = game_state[1]
        self.recent_bet = game_state[2]

        #update the pot and user bank labels
        self.update_pot(pot=self.pot) 
        self.update_user_bank(user_bank=self.user_bank)

        #clear log box and guide box
        self.clear_log()
        if self.tutorial_mode_on == True:
            self.clear_guide()

        #The flop is revealed
        self.community_deck = community_cards(community_deck=self.community_deck, x=3)
        self.log_box.insert(tk.END, f"Revealing the flop\n")

        #clear the frame, but keeping it in the same place
        for widget in self.community_frame.winfo_children(): # Destroy all widgets in the community frame
            widget.destroy()
            
        #Add the community cards to the community frame
        for card in self.community_deck:
            #replace the first 3 back facing cards with the community cards
            rank = card[0] #Get the rank of the card
            suit = card[1] #Get the suit of the card
            image_path = f"cards/{ranks[rank]}_of_{suits[suit]}.png" #Load the image
            self.add_cards_to_deck(frame=self.community_frame,img_path=image_path) #Call the add_cards_to_deck method to add the card to the community deck
        
        # Check if the community deck is not full
        if len(self.community_deck) != 5: # If the community deck is not full
            number_of_cards_needed = 5 - len(self.community_deck) # Calculate the number of cards needed to fill the community deck
            image_path = Image.open("cards/back.jpg") # Open the back image using PIL
            for i in range(number_of_cards_needed): # For each card needed
                self.add_cards_to_deck(frame=self.community_frame,img_path="cards/back.jpg") # Call the add_cards_to_deck method to add the card to the community deck

        # Check if the tutorial mode is enabled, and if so call the action_recommendation method
        if self.tutorial_mode_on == True: 
            self.action_recommendation()

        #Second round of betting
        self.ai_strength = eval_hand(hand1=self.ai_deck, com_cards=self.community_deck)
        if small_blind == True:
            game_state = betting_round_user_first(self.ai_strength, self.pot, self.user_bank, self.recent_bet, self) # Pass the instance of VisualLogic to betting_round_user_first in mainprogram.py
        else:
            game_state = betting_round_ai_first(self.ai_strength, self.pot, self.user_bank, self.recent_bet, self) # Pass the instance of VisualLogic to betting_round_ai_first in mainprogram.py

        # Check if the user folded or the AI folded
        if game_state == "fold":
            self.user_folded() # If the user folds, call the user_folded method
        elif game_state == "ai_folded":
            self.ai_folded() # If the AI folds, call the ai_folded method

        #Redefine the game state variables
        self.pot = game_state[0]
        self.user_bank = game_state[1]
        self.recent_bet = game_state[2]
        
        #update the pot and user bank
        self.update_pot(pot=self.pot)
        self.update_user_bank(user_bank=self.user_bank)

        #clear log box and guide box
        self.clear_log()
        if self.tutorial_mode_on == True:
            self.clear_guide()

        #The turn is revealed
        self.community_deck = community_cards(community_deck=self.community_deck, x=1) # Call the community_cards method to add the turn card to the community deck
        for widget in self.community_frame.winfo_children(): # Destroy all widgets in the community frame
            widget.destroy() 
        
        #Add the turn card to the community frame
        for card in self.community_deck:
            #replace the first 4 back facing cards with the community cards
            rank = card[0] #Get the rank of the card
            suit = card[1] #Get the suit of the card
            image_path = f"cards/{ranks[rank]}_of_{suits[suit]}.png" #Load the image
            self.add_cards_to_deck(frame=self.community_frame,img_path=image_path) #Call the add_cards_to_deck method to add the card to the community deck
    
        # Check if the community deck is not full
        if len(self.community_deck) != 5: # If the community deck is not full
            number_of_cards_needed = 5 - len(self.community_deck) # Calculate the number of cards needed to fill the community deck
            for i in range(number_of_cards_needed): # For each card needed
                self.add_cards_to_deck(frame=self.community_frame,img_path="cards/back.jpg") # Call the add_cards_to_deck method to add the card to the community deck

        # Check if the tutorial mode is enabled, and if so call the action_recommendation method
        if self.tutorial_mode_on == True: # If tutorial mode is enabled
            self.action_recommendation() # Provide action recommendations based on the user's hand strength, by calling the action_recommendation method

        #Third round of betting
        self.ai_strength = eval_hand(hand1=self.ai_deck, com_cards=self.community_deck) # Evaluate the AI's hand strength
        if small_blind == True: # If the user is the small blind
            game_state = betting_round_user_first(self.ai_strength, self.pot, self.user_bank, self.recent_bet, self) # Pass the instance of VisualLogic to betting_round_user_first in mainprogram.py
        else:
            game_state = betting_round_ai_first(self.ai_strength, self.pot, self.user_bank, self.recent_bet, self) # Pass the instance of VisualLogic to betting_round_ai_first in mainprogram.py

        # Check if the user folded or the AI folded
        if game_state == "fold":
            self.user_folded()
        elif game_state == "ai_folded":
            self.ai_folded()
        
        #Redefine the game state variables
        self.pot = game_state[0]
        self.user_bank = game_state[1]
        self.recent_bet = game_state[2]

        #update the pot and user bank
        self.update_pot(pot=self.pot)
        self.update_user_bank(user_bank=self.user_bank)
        
        #clear log box and guide box
        self.log_box.delete(1.0, tk.END)
        if self.tutorial_mode_on == True:
            self.guide_box.delete(1.0, tk.END)

        #The river is revealed
        self.community_deck = community_cards(community_deck=self.community_deck, x=1) # Call the community_cards method to add the river card to the community deck
        self.log_box.insert(tk.END, f"Revealing the river\n") # Output in log box the action done

        #Clear the frame but keep it in same place 
        for widget in self.community_frame.winfo_children(): # Destroy all widgets in the community frame
            widget.destroy()
        
        #Add the river card to the community frame
        for card in self.community_deck:
            #replace the 5 back facing cards with the community cards
            rank = card[0] #Get the rank of the card
            suit = card[1] #Get the suit of the card
            image_path = f"cards/{ranks[rank]}_of_{suits[suit]}.png" #Load the image
            self.add_cards_to_deck(frame=self.community_frame,img_path=image_path) #Call the add_cards_to_deck method to add the card to the community deck
        
        # Check if the community deck is not full
        self.user_hand_strength = eval_hand(hand1=self.user_deck, com_cards=self.community_deck)
        if self.tutorial_mode_on == True:
            self.action_recommendation() # Provide action recommendations based on the user's hand strength, by calling the action_recommendation method

        #final round of betting
        self.ai_strength = eval_hand(hand1=self.ai_deck, com_cards=self.community_deck) # Evaluate the AI's hand strength
        if small_blind == True: # If the user is the small blind
            game_state = betting_round_user_first(self.ai_strength, self.pot, self.user_bank, self.recent_bet, self) # Pass the instance of VisualLogic to betting_round_user_first in mainprogram.py
        else: 
            game_state = betting_round_ai_first(self.ai_strength, self.pot, self.user_bank, self.recent_bet, self) # Pass the instance of VisualLogic to betting_round_ai_first in mainprogram.py

        # Check if the user folded or the AI folded
        if game_state == "fold":
            self.user_folded()
        elif game_state == "ai_folded":
            self.ai_folded()

        #Redefine the game state variables
        self.pot = game_state[0]
        self.user_bank = game_state[1]
        self.recent_bet = game_state[2]

        #update the pot and user bank
        self.update_pot(pot=self.pot)
        self.update_user_bank(user_bank=self.user_bank)
        
        #clear log box and guide box
        self.log_box.delete(1.0, tk.END)
        if self.tutorial_mode_on == True:
            self.guide_box.delete(1.0, tk.END)

        #reveal ai cards
        for widget in self.ai_frame.winfo_children(): # Destroy all widgets in the AI frame
            widget.destroy()
        
        for card in self.ai_deck: # For each card in the AI deck
            rank = card[0] # Get the rank of the card
            suit = card[1] # Get the suit of the card
            image_path = f"cards/{ranks[rank]}_of_{suits[suit]}.png" # Load the image
            self.add_cards_to_deck(frame=self.ai_frame,img_path=image_path) # Call the add_cards_to_deck method to add the card to the AI deck

        # Determine winner
        self.login_system = LoginClass() # Reuse the login_system instance
        result_function(self.user_deck, self.ai_deck, self.community_deck, self.pot, self.username, self.user_bank, visual_logic=self,login_system=self.login_system) # Call the result_function to determine the winner and update the user bank

        #Play again?
        self.ask_to_play_again()