class player:

    def __init__(self,name1,score1,team1):
        self.name = name1
        self.score = score1
        self.team = team1

    def show_stats(self):
        return self.name, self.score, self.team

    def select_team(self):
        value = input("Enter value of team: ")
        return value
    
        

        
