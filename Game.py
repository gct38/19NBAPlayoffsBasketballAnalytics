from operator import itemgetter
from Player import Player
from StartingLineup import StartingLineup
from EventCodes import parseEventCodes
from EventCodes import searchEventCodes

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
            self.play.append(temp)
        #sort by Period (ascending), PC_Time (descending), WC_Time (ascending), Event_Num(ascending)
        self.play = sorted(self.play, key = itemgetter("Event_Num"))
        self.play = sorted(self.play, key = itemgetter("WC_Time"))
        self.play = sorted(self.play, key = itemgetter("PC_Time"), reverse = True)
        self.play = sorted(self.play, key = itemgetter("Period"))

    #goes through each play and calculates defensive and offensive ratings of each player
    #TODO: implement function
    def ratings(self):
        for i in range(len(self.play)):
            if self.play[i]['Period'] != self.currentPeriod and self.play[i]['Event_Msg_Type'] == 12 and self.play[i]['Action_Type'] == 0:
                self.currentPeriod = self.play[i]['Period']
                #update lineup with new period

            if i == len(self.play)-1:
                end_of_possession(self.play[i])
            else:
                end_of_possession(self.play[i], self.play[i+1])

    #TODO: implement helper function for substitutions/figure out who the starters are for each period
    #       was thinking of looking through play by play and find out the first 5 people substituted OUT
    #       for each team would be the team's starters. Need to make sure that this is a valid assumption.
    #       From there I would have the 10 people currently on the floor at all times and manage it through substitution.
    #       It seems like Game Lineup doesn't really help that much at all in determining the starters.


#parses thru Game_Lineup.csv file and returns a dict (key = gameid, value = Game object)
def parseGameLineup(filename):
    game = dict()
    filename = open(filename, encoding = "ISO-8859-1")
    filename.readline()
    gameId = ""
    aGame = []
    counter = 0
    for line in filename:
        line = line.replace("\"","").strip().split('\t')
        if gameId == "":
            gameId = line[0].strip()
            aGame.append(line)
        elif gameId != line[0].strip():
            game[gameId] = Game(aGame)
            gameId = line[0].strip()
            aGame = [line]
        else:
            aGame.append(line)
    game[gameId] = Game(aGame)
    return game

#END OF POSSESSION REQUIREMENTS
'''
    Can end either 6 diff ways:
    1) Made Field Goal Attempt
    2) Made Final Free Throw Attempt
    3) Missed Final Free Throw Attempt that results in DEFENSIVE rebound
    4) Missed Field Goal attempt that results in a DEFENSIVE rebound
    5) Turnover
    6) End of Time Period
'''
#TODO: test to make sure this is working correctly
#returns a phrase of what the end of possession is or None (not an end of posssession)
#maybe have it return tuple, (True/False, pt value to add?) [T/F is used to determine whether or not possession ended]
#                           pt value to add then adds onto each player's (its own object) ptsScored/ptsAllowed properties
#                           if True, add 1 to every player's possession property, else ignore
def end_of_possession(play, next_play=None):
    event_msg_type = play['Event_Msg_Type']
    action_type = play['Action_Type']
    madeFieldGoalAttempt =  event_msg_type == 1 #made field goal attempt
    turnover = event_msg_type == 5 #turnover
    endOfTime = event_msg_type == 13  #end of time period
    if madeFieldGoalAttempt:
        return "Made Field Goal Attempt"
    elif turnover:
        return "Turnover"
    elif endOfTime:
        return "End of Time Period"
    elif next_play is not None:
        next_event_msg_type = next_play['Event_Msg_Type']
        madeFinalFreeThrow = (event_msg_type == 3) and (
                    action_type == 10 or action_type == 12 or action_type == 15 or action_type == 19 or
                    action_type == 20 or action_type == 22 or action_type == 26 or action_type == 29) and \
                             (
                                         next_event_msg_type != 4)  # made final free throw attempt
        missedFreeThrowRebound = (event_msg_type == 3) and (
                    action_type == 10 or action_type == 12 or action_type == 15 or action_type == 19 or
                    action_type == 20 or action_type == 22 or action_type == 26 or action_type == 29) and (
                                             next_event_msg_type == 4)
        missedFieldGoalRebound = (event_msg_type == 2) and (
                    next_event_msg_type == 4)  # missed shot and defensive rebound
        if madeFinalFreeThrow:
            return "Made Final Free Throw"
        elif missedFreeThrowRebound:
            return "Missed Free Throw Defensive Rebound"
        elif missedFieldGoalRebound:
            return "Missed Field Goal Defensive Rebound"
    return None
