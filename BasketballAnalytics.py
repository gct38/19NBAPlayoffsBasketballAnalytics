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

    def print(self):
        print(self.__str__())

    def __str__(self):
        message = ""
        for key in self.eventMsg:
            message += "Event Message: " + self.eventMsg[key] + ","
        for key in self.actionType:
            message += " Action Type: " + self.actionType[key]
        return message


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
        self.currentLineup = self.populateLineup()
        self.playbyplay = None

    def populatePlayers(self):
        players = dict()
        for period in self.startingLineup.lineup:
            for team in self.startingLineup.lineup[period]:
                for status in self.startingLineup.lineup[period][team]:
                    for player in self.startingLineup.lineup[period][team][status]:
                        if player not in players:
                            players[player] = Player(player)
        return players

    def populateLineup(self):
        lineup = dict()
        for team in self.startingLineup.lineup[1]:
            lineup[team] = self.startingLineup.lineup[1][team]["A"]
        return lineup

    def populatePlays(self, plays):
        self.playbyplay = PlayByPlay(plays)


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

#plays is list of every play in a game (2D list)
#[game_id, event_num, event_msg_type, period, WC_time, PC_Time, Action_Type, Option1, Option2, Option3,
#              Team_id, Person1, Person2, Person3, Team_id_type, Person1_type, Person2_type, Person3_type]
#   Don't need game_id (0),Team_id(10), Team_id_type(14), Person1_type(15), Person2_type(16), Person3_type(17)
# TODO: finish PlayByPlay class __init__ method
class PlayByPlay:
    def __init__(self, plays):
        self.play = 0




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
class Player:
    def __init__(self, playerId):
        self.playerId = str(playerId).strip()
        self.defRtg = 0
        self.offRtg = 0
        self.possessions = 0
        self.pointsAllowed = 0
        self.pointsScored = 0

    def calculateRtg(self):
        self.offRtg = self.pointsScored/self.possessions
        self.defRtg = self.pointsAllowed/self.possessions



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
    game = dict()
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
            game[gameId] = Game(aGame)
            gameId = line[0].strip()
            aGame = [line]
        else:
            aGame.append(line)
    return game




if __name__ == "__main__":


    ##testing area
        #testing EventCodes class object
    eventCodes = parseEventCodes("Event_Codes.txt")
    event = searchEventCodes(eventCodes, 12,0)
    if event != None:
        event.print()
        print(event)
        print(event.eventMsg)
        print(event.actionType)
    else:
        print("could not find")

        #testing Game, StartingLineup, Player, Rating class objects
    games = parseGameLineup("Game_Lineup.txt")

    print(len(games))
    print(games["006728e4c10e957011e1f24878e6054a"].gameId)
    print(games["006728e4c10e957011e1f24878e6054a"].teams)
    print(len(games["006728e4c10e957011e1f24878e6054a"].players))


    counter = 0
    for team in games["006728e4c10e957011e1f24878e6054a"].startingLineup.lineup[0]:
        for status in games["006728e4c10e957011e1f24878e6054a"].startingLineup.lineup[0][team]:
            for person in games["006728e4c10e957011e1f24878e6054a"].startingLineup.lineup[0][team][status]:
                print(person)
                counter += 1

    print(counter)

    print(games["006728e4c10e957011e1f24878e6054a"].playbyplay)
    for team in games["006728e4c10e957011e1f24878e6054a"].currentLineup:
        print(team)
        print(games["006728e4c10e957011e1f24878e6054a"].currentLineup[team])

    '''
    for player in games["006728e4c10e957011e1f24878e6054a"].players:
        print(player, games["006728e4c10e957011e1f24878e6054a"].players[player].playerId)
    '''


    ##parsing play_by_play.txt file
    #[game_id, event_num, event_msg_type, period, WC_time, PC_Time, Action_Type, Option1, Option2, Option3,
#              Team_id, Person1, Person2, Person3, Team_id_type, Person1_type, Person2_type, Person3_type]
    #   Don't need game_id (0),Team_id(10), Team_id_type(14), Person1_type(15), Person2_type(16), Person3_type(17)
    playbyplay = open("Play_by_Play.txt", encoding = "ISO-8859-1")
    playbyplay.readline()
    gameId = ""
    aGame = []
    for line in playbyplay:
        line = line.replace("\"","").strip().split('\t')
        if gameId == "":
            gameId = line[0].strip()
            aGame.append(line[1:10] + line[11:14])
        elif gameId != line[0].strip():
            games[gameId].populatePlays(aGame)
            gameId = line[0].strip()
            aGame = [line[1:10] + line[11:14]]
        else:
            aGame.append(line[1:10] + line[11:14])







