from operator import itemgetter
from Player import Player
from StartingLineup import StartingLineup
from EventCodes import parseEventCodes
from EventCodes import searchEventCodes


#TODO: get rid of all test code/print statements

#game is going to be a list of every game
#   each game consists of [game_id, period, person_id, team_id, status]
#plays is list of every play in a game (2D list)
#   each play consists of [event_num, event_msg_type, period, WC_time, PC_Time, Action_Type, Option1, Option2, Option3, Team_id, Person1, Person2, Person3]
#   sorted in order of: Period (ascending), PC_Time (descending), WC_Time (ascending), Event_Num(ascending)
'''
Properties:
1) gameId = the game id, str
2) teams = teams playing in game, list
3) startingLineups = starting lineup for all periods in the game, StartingLineup object
4) players = all the players in the game, dict; key=playerId, value=Player object
5) currentLineup = current lineup for both teams at the moment
6) subLineup = lineup to be substituted in
6) play = all the plays for the game, list of each play as a dict (sorted properly) 
7) currentPeriod = tracks the current period of the game
'''
class Game:
    def __init__(self, game):
        self.gameId = str(game[0][0]).strip()
        self.teams = self.__populateTeams(game)
        self.startingLineups = StartingLineup(game) #starting lineup for every period (need to fix players for period0)
        self.players = self.__populatePlayers()
        self.currentLineup = self.startingLineups.lineup[1] #initialize to starting lineup
        self.subLineup = self.currentLineup
        self.play = None
        self.currentPeriod = 0

    #populates teams property
    def __populateTeams(self, game):
        teams = []
        for item in game:
            teamId = str(item[3]).strip()
            if teamId not in teams:
                teams.append(teamId)
        return teams

    #populates players property
    def __populatePlayers(self):
        players = dict()
        for period in self.startingLineups.lineup:
            for team in self.startingLineups.lineup[period]:
                for player in self.startingLineups.lineup[period][team]:
                    if player not in players:
                        players[player] = Player(player, team)
        return players

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
    #TODO: testing function
    def ratings(self):
        freeThrow = False
        startfreeThrow = False
        for i in range(len(self.play)):
            #updating currentLineup and period
            if self.play[i]['Period'] != self.currentPeriod and self.play[i]['Event_Msg_Type'] == 12 and self.play[i]['Action_Type'] == 0:
                #print('NEW LINEUP Period:', self.currentPeriod, "new period:", self.currentPeriod + 1)
                #print('old lineup:', self.currentLineup)
                self.currentPeriod = self.play[i]['Period']
                self.currentLineup = self.startingLineups.lineup[self.currentPeriod] #update lineup with new period
                #print('new lineup:', self.currentLineup)
                #print()

            #check to see if end of possession
            if i == len(self.play)-1:
                eop, pts = end_of_possession(self.play[i])
            else:
                eop, pts = end_of_possession(self.play[i], self.play[i+1])

            #checking if in free throw sequence
            if freeThrow:
                if eop:        #if free throw sequence finished, then reset freeThrow bool to False
                    freeThrow = False
            else:               #if not in free throw sequence, check to see if it is now
                freeThrow = free_throw(self.play[i])        #bool of whether or not in middle of free throw sequence
                if freeThrow:   #only set this True whenever freeThrow goes from False to True
                    startfreeThrow = True

            self.__substitution(self.play[i], freeThrow, eop, startfreeThrow)   #substitute players
            startfreeThrow = False #when do I reset this bool back to False?

            if pts != 0:
                self.__rpm(self.players[self.play[i]['Person1']].teamId, pts)      #adding to players off/def ratings

        self.__calculate_ratings()      #used to calculate every player's off/def rating per 100 possessions in the game





    #TODO: test that substitutions helper function to swap players out (make sure to account for free throws)
    #helper function to substitute players
    def __substitution(self, play, freeThrow, eop, start):
        if play['Event_Msg_Type'] != 8 or play['Event_Msg_Type'] != 3: #making sure it is a substitution play
            return
        personOut = play['Person1']
        personIn = play['Person2']
        team = self.players[personIn].teamId
        #print("person in:", personIn, "person Out:", personOut, "team:", team, "play:", play)
        #print('bools', freeThrow, eop, start, 'play', play)
        #print('prev sublineup',self.subLineup)

        #substitution sequences
        if not freeThrow:                                       #not a free throw sequence
            self.currentLineup[team].remove(personOut)
            self.currentLineup[team].append(personIn)
        elif freeThrow and start:                               #start of free throw
            self.subLineup = self.currentLineup
            #print('after sublineup', self.subLineup)
        elif freeThrow and not start:                           #middle of free throw
            self.subLineup[team].remove(personOut)
            self.subLineup[team].append(personIn)
        elif eop:                                               #end of free throw sequence
            #eop means end of possession which signifies that it ended the free throw sequence
            self.currentLineup = self.subLineup



    #will add to off/def rating of the individual player if they're in the currentLineup
    def __rpm(self, addTeam, pts):
        for team in self.currentLineup:
            for playerId in self.currentLineup[team]:
                if team == addTeam:
                    self.players[playerId] + pts
                else:
                    self.players[playerId] - pts

    #helper function to calculate everyone's off/def rating per 100 possessions
    def __calculate_ratings(self):
        for player in self.players:
            self.players[player].calculateRtg()


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
#returns a tuple, (True/False, pt value to add) [T/F is used to determine whether or not possession ended]
#                           pt value to add then adds onto each player's (its own object) ptsScored/ptsAllowed properties
#                           if True, add 1 to every player's possession property, else ignore
def end_of_possession(play, next_play=None):
    event_msg_type = play['Event_Msg_Type']
    action_type = play['Action_Type']
    pt_value = play['Option1']
    madeFieldGoalAttempt =  event_msg_type == 1 #made field goal attempt
    turnover = event_msg_type == 5 #turnover
    endOfTime = event_msg_type == 13  #end of time period
    madeFinalFreeThrow = (event_msg_type == 3) and (
            action_type == 10 or action_type == 12 or action_type == 15 or action_type == 19 or
            action_type == 20 or action_type == 22 or action_type == 26 or action_type == 29) and (play['Option1'] != 0)  # made final free throw attempt
    if madeFieldGoalAttempt:
        return True, pt_value    # field goal pt value
    elif turnover:
        return True, 0                  # turnover doesn't result in any pts
    elif endOfTime:
        return True, 0                  # end of a period doesn't result in any pts
    elif madeFinalFreeThrow:
        return True, pt_value
    elif next_play is not None:
        next_event_msg_type = next_play['Event_Msg_Type']
        next_pt_value = next_play['Option1']
        missedFreeThrowRebound = (event_msg_type == 3) and (next_pt_value == 0) and (
                    action_type == 10 or action_type == 12 or action_type == 15 or action_type == 19 or
                    action_type == 20 or action_type == 22 or action_type == 26 or action_type == 29) and (next_event_msg_type == 4) # missed free throw that results in defensive rebound
        missedFieldGoalRebound = (event_msg_type == 2) and (next_event_msg_type == 4)  # missed shot and defensive rebound
        if missedFreeThrowRebound:
            return True, 0              # missed free throw is 0 pts
        elif missedFieldGoalRebound:
            return True, 0              # missed field goal is 0 pts
    return False, 0                     # not an end of possession


#helper function to determine if it's a free throw sequence (used for substitution/scoring purposes)
#returns True if current play is a free throw, but not the last free throw
def free_throw(play):
    freeThrow = play['Event_Msg_Type'] == 3
    last_freeThrow = (play['Action_Type'] == 10) or (play['Action_Type'] == 12) or (play['Action_Type'] == 15) or (play['Action_Type'] == 16) or \
                     (play['Action_Type'] == 17) or (play['Action_Type'] == 19) or (play['Action_Type'] == 20) or (play['Action_Type'] == 22) or \
                     (play['Action_Type'] == 26) or (play['Action_Type'] == 29)
    return freeThrow and not last_freeThrow
