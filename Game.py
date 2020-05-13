from operator import itemgetter
from Player import Player
from StartingLineup import StartingLineup

#game is going to be a list of every game
#   each game consists of [game_id, period, person_id, team_id, status]
#plays is list of every play in a game (2D list)
#   each play consists of [event_num, event_msg_type, period, WC_time, PC_Time, Action_Type, Option1, Option2, Option3, Team_id, Person1, Person2, Person3]
#   sorted in order of: Period (ascending), PC_Time (descending), WC_Time (ascending), Event_Num(ascending)
'''
Properties:
1) gameId = the game id, str
2) teams = teams playing in game, list
3) startingLineup = starting lineup for all periods in the game, StartingLineup object
4) players = all the players in the game, dict; key=playerId, value=Player object
5) currentLineup = current lineup for both teams at the moment
6) play = all the plays for the game, list of each play as a dict (sorted properly) 
7) currentPeriod = tracks the current period of the game
'''
class Game:
    def __init__(self, game):
        gameId = str(game[0][0]).strip()
        self.gameId = gameId
        self.teams = []
        for item in game:
            teamId = str(item[3]).strip()
            if teamId not in self.teams:
                self.teams.append(teamId)
        self.startingLineup = StartingLineup(game)
        self.players = self.populatePlayers()
        self.currentLineup = self.populateLineup()
        self.play = None
        self.currentPeriod = 0

    #populates players property
    def populatePlayers(self):
        players = dict()
        for period in self.startingLineup.lineup:
            for team in self.startingLineup.lineup[period]:
                for status in self.startingLineup.lineup[period][team]:
                    for player in self.startingLineup.lineup[period][team][status]:
                        if player not in players:
                            players[player] = Player(player, team)
        return players

    #returns the lineup in a game
    #TODO: I don't think this works
    def populateLineup(self):
        lineup = dict()
        for team in self.startingLineup.lineup[1]:
            lineup[team] = self.startingLineup.lineup[1][team]["A"]
        return lineup

    #populates play property with all the plays in a game
    def populatePlays(self, plays):
        self.play = []
        #print('Plays:', len(plays), self.gameId) TODO: delete this test line
        for play in plays:
            temp = dict()
            temp["Event_Num"] = int(play[0].replace("\"","").strip())
            temp["Event_Msg_Type"] = int(play[1].replace("\"","").strip())
            temp["Period"] = int(play[2].replace("\"","").strip())
            temp["WC_Time"] = int(play[3].replace("\"","").strip())
            temp["PC_Time"] = int(play[4].replace("\"","").strip())
            temp["Action_Type"] = int(play[5].replace("\"","").strip())
            temp["Option1"] = int(play[6].replace("\"","").strip())
            temp["Option2"] = int(play[7].replace("\"","").strip())
            temp["Option3"] = int(play[8].replace("\"","").strip())
            temp["Person1"] = str(play[9].replace("\"","")).strip()
            temp["Person2"] = str(play[10].replace("\"","")).strip()
            temp["Person3"] = str(play[11].replace("\"","")).strip()
            #print('Counter:', counter, play) TODO: delete this test line
            self.play.append(temp)
        #sort by Period (ascending), PC_Time (descending), WC_Time (ascending), Event_Num(ascending)
        self.play = sorted(self.play, key = itemgetter("Event_Num"))
        self.play = sorted(self.play, key = itemgetter("WC_Time"))
        self.play = sorted(self.play, key = itemgetter("PC_Time"), reverse = True)
        self.play = sorted(self.play, key = itemgetter("Period"))

    #goes through each play and calculates defensive and offensive ratings of each player
    #TODO: implement function
    def ratings(self):
        for play in self.play:
            if play['Period'] != self.currentPeriod and play['Event_Msg_Type'] == 12 and play['Action_Type'] == 0:
                self.currentPeriod = play['Period']
                #update lineup with new period
            if play['Option3'] != 0:
                print(play)

