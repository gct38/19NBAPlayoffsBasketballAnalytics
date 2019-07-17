import csv

#TODO: create some type of data structure that'll hold the game_lineup data,
# just create a parsing func that will return some type of data structure

#class to help better organize all Event Codes
class EventCodes:
    def __init__(self, EventCodesLine):
        self.eventMsg = dict()
        self.eventMsg[int(EventCodesLine[0].strip())] = str(EventCodesLine[2]).strip()
        self.actionType = dict()
        self.actionType[int(EventCodesLine[1].strip())] = str(EventCodesLine[3]).strip()


#teams is a dict(), keys rep which team; values rep list of players for that team
#TODO:how to globally access the end all be all for players and their off/def rtg??????
#  maybe have a func that will return list of all players as a Player object??
#TODO: implement __getitem__ method override to allow for indexing of something, will figure out what later
class Game:
    def __init__(self, game):
        self.gameId = str(game[0]).strip()
        self.teams = dict()
        period = int(game[1].strip())
        personId = str(game[2]).strip()
        teamId = str(game[3]).strip()
        status = str(game[4]).strip()
        if status == "I" and period == 0: #TODO: double check criteria for being inactive for entire game
            self.teams[teamId] = [Player(personId, self.gameId)]
            # FIXME: the above code is temp until figure out what to do ^^
        else:
            self.teams[teamId] = [Player(personId, self.gameId)]

        # TODO: implement startingLineups list of all starting lineups for every period
        #   startingLineups is supposed to carry all the starting lineups for each game and team
        self.startingLineups = [[period, teamId, personId, status]]

    ##called when gameid is same, so will have to add in this new line's info
    def AddToGame(self, line):
        period = int(line[1].strip())
        personId = str(line[2]).strip()
        teamId = str(line[3]).strip()
        status = str(line[4]).strip()
        self.teams[teamId].append(Player(personId, self.gameId))
        #if period not in startingLineups
        self.startingLineups.append([period, teamId, personId, status])




#TODO: test to ensure this class is working properly
class Player:
    def __init__(self, playerId, gameId):
        self.playerId = str(playerId).strip()
        self.defRtg = 0
        self.offRtg = 0
        self.games = dict()
        self.games[str(gameId).strip()] = [0,0] #list is supposed to rep offRtg,defRtg of player in that game, respectively



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

#returns a EventCodes object
def searchEventCodes(eventCodes, eventMsg, actionType):
    eventMsg = int(eventMsg)
    actionType = int(actionType)
    for event in eventCodes:
        if eventMsg in event.eventMsg and actionType in event.actionType:
            return event
        else:
            continue
    return None




if __name__ == "__main__":
    ##testing area
    eventCodes = parseEventCodes("Event_Codes.txt")
    event = searchEventCodes(eventCodes, 15,32)
    if event != None:
        print(event.eventMsg)
        print(event.actionType)
    else:
        print("could not find")


