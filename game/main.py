from cli import CommandLineGame

if __name__ == "__main__":
    game = CommandLineGame(master=None)
    game.login_loop()