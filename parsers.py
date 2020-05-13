from Game import Game
from EventCodes import EventCodes

#parse thru Event_Codes.csv file and returns a list of EventCodes objects
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

#parses Play_by_Play.csv file and updates the games dict
def parsePlayByPlay(filename, games):
    filename = open(filename, encoding = "ISO-8859-1")
    filename.readline()
    gameId = ""
    aGame = []
    for line in filename:
        line = line.strip().split('\t')
        if gameId == "":
            gameId = line[0].replace("\"","").strip()
            aGame.append(line[1:10] + line[11:14])
        elif gameId != line[0].replace("\"","").strip():
            games[gameId].populatePlays(aGame)
            #print('Game ID:', gameId, 'curr GameID:', line[0].replace("\"","").strip(), 'bool', gameId != line[0].replace("\"","").strip(), 'aGame:', aGame) TODO: delete test line
            gameId = line[0].replace("\"","").strip()
            aGame = [line[1:10] + line[11:14]]
        else:
            aGame.append(line[1:10] + line[11:14])
    games[gameId].populatePlays(aGame)
