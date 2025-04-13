# This is a simple login system that allows users to register and login.
# It uses a JSON file to store user details and passwords are hashed for security.
# The system also allows for updating the user's bank balance.
# The class LoginClass handles all the login and registration logic.
# It uses the hashlib library to hash passwords and the json library to read and write user data.
# The class also includes methods for loading user data, saving user data, and updating the user's bank balance.
# This code is part of a login system for a poker game. It allows users to register, login, and manage their bank balance.

import hashlib,json
class LoginClass: # Class for the login system
    def __init__(self,filename="logindetails.json"): # Constructor
        self.filename = filename 
        self.users = self.load_file() # Load user data from the JSON file
        self.current_user = None 

    def load_file(self): # Method for loading user data from the JSON file
        try: # Open the file and read the data
            with open(self.filename, 'r') as file: # Read the file
                return json.load(file) # Load the data into a dictionary
        except FileNotFoundError: 
            return {} # If the file does not exist, return an empty dictionary

    def register(self, username, password): # Method for registering a new user
        password = hashlib.sha256(password.encode()).hexdigest() # Hash the password
        if username in self.users: # Check if the username already exists
            return("Unsuccessful registration: Username already exists")
        else: # If the username does not exist, add it to the dictionary
            self.users[username] = {'password': password, 'chips': 500} # Default chips amount
            self.save_users() # Save the user data to the JSON file
            return("Registration successful")

    def login(self, username, password): # Method for logging in a user
        password = hashlib.sha256(password.encode()).hexdigest() # Hash the password
        if self.users.get(username) and self.users[username]['password'] == password: # Check if the username and password match
            self.current_user = username  # Ensure current_user is set
            arr2 = [username, round(self.users[username]['chips'])] # Get the username and chips amount
            return arr2 # Successful login
        else:
            return False # Unsuccessful login
     
    def save_users(self): # Method for saving user data to the JSON file
        with open(self.filename, "w") as file: # Write the data to the file
            json.dump(self.users, file, indent=4) # Save the data in a readable format
        #print(f"Data saved to {'logindetails.json'}.")

    def update_bank(self,username, user_bank): # Method for updating the user's bank balance
        if user_bank < 0: # Check if the bank balance is negative
            user_bank = 0 # Set it to 0 if it is negative
        self.users[username]['chips'] = user_bank # Update the user's bank balance
        self.save_users() # Save the updated data to the JSON file
    
    def get_username(self): # Method for getting the current user's username
        # Ensure current_user is returned correctly
        if self.current_user: # Check if a user is logged in
            return self.current_user
        else:
            raise ValueError("No user is currently logged in.")


