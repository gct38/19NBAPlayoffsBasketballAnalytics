import csv


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
##  Notes:
# TODO: what's left: parse the play_by_play.txt file and tie it into Game class!!
#   look for Game object by its gameId
#To properly sort the events in a game, use the following sequence of sorted columns:
# Period (ascending), PC_Time (descending), WC_Time (ascending), Event_Num(ascending)


#Use # of possessions to see if user is actually active in that game???

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
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


#class to help better organize all Event Codes
class EventCodes:
    def __init__(self, EventCodesLine):
        self.eventMsg = dict()
        self.eventMsg[int(EventCodesLine[0].strip())] = str(EventCodesLine[2]).strip()
        self.actionType = dict()
        self.actionType[int(EventCodesLine[1].strip())] = str(EventCodesLine[3]).strip()


###################################################################################################################################
###################################################################################################################################
###################################################################################################################################
#game is going to be a list of every game
#   each game consists of [game_id, period, person_id, team_id, status]
'''
Properties:
1) gameId = the game id, str
2) teams = teams playing in game, list
3) startingLineup = starting lineup for all periods in the game, StartingLineup object
4) players = all the players in the game, dict; key=playerId, value=Player object
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

    def populatePlayers(self):
        players = dict()
        for period in self.startingLineup.lineup:
            for team in self.startingLineup.lineup[period]:
                for status in self.startingLineup.lineup[period][team]:
                    for player in self.startingLineup.lineup[period][team][status]:
                        if player not in players:
                            players[player] = Player(player, self.gameId)
        '''
        for player in self.startingLineup.inactives:
            if player in players:
                del players[player]
        '''
        return players



class StartingLineup:
    #properties:
    '''
    self.lineup = dict()
    self.lineup[period] = dict()
    self.lineup[period][team] = status (I or A)
    self.lineup[period][team][status] = [players of status]

    '''
    #game is a list of [game_id, period, person_id, team_id, status] for the entire game
    def __init__(self, game):
        self.lineup = dict()
        #self.inactives = []

        for item in game:
            period = int(item[1].strip())
            person = str(item[2]).strip()
            team = str(item[3]).strip()
            status = str(item[4]).strip().upper()

            if period not in self.lineup:
                self.lineup[period] = dict()
                self.lineup[period][team] = dict()
                self.lineup[period][team][status] = [person]
            else:
                if team not in self.lineup[period]:
                    self.lineup[period][team] = dict()
                    self.lineup[period][team][status] = [person]
                else:
                    if status not in self.lineup[period][team]:
                        self.lineup[period][team][status] = [person]
                    else:
                        self.lineup[period][team][status].append(person)
                        '''
                        if period == 4 and status == "I":
                            if person in self.lineup[0][team]["I"] and person in self.lineup[1][team]["I"] and person in self.lineup[2][team]["I"] and person in self.lineup[3][team]["I"]:
                                #player is now inactive for all 4 periods
                                self.lineup[0][team]["I"].remove(person)
                                self.lineup[1][team]["I"].remove(person)
                                self.lineup[2][team]["I"].remove(person)
                                self.lineup[3][team]["I"].remove(person)
                                self.inactives.append(person)
                        else:
                            self.lineup[period][team][status].append(person)
                        '''


###################################################################################################################################
###################################################################################################################################
###################################################################################################################################

'''
    Properties:
    playerId = player's ID (string)
    defRtg = def rating for the game
    offRtg = off rating for the game
    possessions = # possessions player was active for in the game,
'''
# TODO: make sure that i don't need to split into off possessions and def possessions
class Player:
    def __init__(self, playerId, gameId):
        self.playerId = str(playerId).strip()
        self.defRtg = 0
        self.offRtg = 0
        self.possessions = 0



def parseEventCodes(filename):
    eventCodes = list()
    filename = open(filename, encoding = "ISO-8859-1")
    filename.readline()
    for line in filename:
        line = line.replace("\"","").strip().split("\t")
        if len(line) < 4:
            line.append("")
        eventCodes.append(EventCodes(line))
    return eventCodes

#search function that returns a EventCodes object
def searchEventCodes(eventCodes, eventMsg, actionType):
    eventMsg = int(eventMsg)
    actionType = int(actionType)
    for event in eventCodes:
        if eventMsg in event.eventMsg and actionType in event.actionType:
            return event
        else:
            continue
    return None

def parseGameLineup(filename):
    game = list()
    filename = open(filename, encoding = "ISO-8859-1")
    filename.readline()
    gameId = ""
    aGame = []
    for line in filename:
        line = line.replace("\"","").strip().split('\t')
        if gameId == "":
            gameId = line[0].strip()
            aGame.append(line)
        elif gameId != line[0].strip():
            game.append(Game(aGame))
            gameId = line[0].strip()
            aGame = [line]
        else:
            aGame.append(line)
    return game



if __name__ == "__main__":


    ##testing area
        #testing EventCodes class object
    eventCodes = parseEventCodes("Event_Codes.txt")
    event = searchEventCodes(eventCodes, 15,32)
    if event != None:
        print(event.eventMsg)
        print(event.actionType)
    else:
        print("could not find")

        #testing Game, StartingLineup, Player, Rating class objects
    games = parseGameLineup("Game_Lineup.txt")

    print(len(games))
    print(games[0].gameId)
    print(games[0].teams)
    print(len(games[0].players))

    '''
    counter = 0
    for team in games[0].startingLineup.lineup[0]:
        for status in games[0].startingLineup.lineup[0][team]:
            for person in games[0].startingLineup.lineup[0][team][status]:
                print(person)
                counter += 1

    print(counter)
    
    for player in games[0].players:
        print(player, games[0].players[player].playerId)
    '''







