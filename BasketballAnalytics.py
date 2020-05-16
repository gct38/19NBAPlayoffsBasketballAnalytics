#TODO: phase out parsers file
from EventCodes import searchEventCodes
from Game import parseGameLineup
#from Game import parsePlayByPlay
import csv


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
##  Notes:
#Use # of possessions to see if user is actually active in that game???
#       because you can rack up DNP-Coach's Decisions

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
            gameId = line[0].replace("\"","").strip()
            aGame = [line[1:10] + line[11:14]]
        else:
            aGame.append(line[1:10] + line[11:14])
    games[gameId].populatePlays(aGame)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

if __name__ == "__main__":
    ##testing area
        #testing EventCodes class object
    '''
    eventCodes = parseEventCodes("Event_Codes.txt")
    event = searchEventCodes(eventCodes, 12,0)
    if event != None:
        event.print()
        print(event)
        print(event.eventMsg)
        print(event.actionType)
    else:
        print("could not find")
    print()
    print()
    '''
        #testing Game, StartingLineup, Player, Rating class objects
    games = parseGameLineup("Game_Lineup.txt")
    parsePlayByPlay("Play_by_Play.txt", games)

    #TODO: Game.players property; what is Option3?
    print(len(games))
    print(games["006728e4c10e957011e1f24878e6054a"].gameId)
    print(games["006728e4c10e957011e1f24878e6054a"].teams)
    print(len(games["006728e4c10e957011e1f24878e6054a"].players))
    curr_game = games["006728e4c10e957011e1f24878e6054a"]
    #curr_game.ratings()
    #players = curr_game.players
    #a = curr_game.helper()
    #print(a)
    print(curr_game.players)
    #print(curr_game.players['0370a0d090da0d0edc6319f120187e0e'])
    '''
    counter = 0
    for team in games["006728e4c10e957011e1f24878e6054a"].startingLineup.lineup[0]:
        for status in games["006728e4c10e957011e1f24878e6054a"].startingLineup.lineup[0][team]:
            for person in games["006728e4c10e957011e1f24878e6054a"].startingLineup.lineup[0][team][status]:
                print(person)
                counter += 1

    print(counter)

    print(games["006728e4c10e957011e1f24878e6054a"].play)
    for team in games["006728e4c10e957011e1f24878e6054a"].currentLineup:
        print(team)
        print(games["006728e4c10e957011e1f24878e6054a"].currentLineup[team])

    
    for player in games["006728e4c10e957011e1f24878e6054a"].players:
        print(player, games["006728e4c10e957011e1f24878e6054a"].players[player].playerId)
    '''


    ##parsing play_by_play.txt file
    #[game_id, event_num, event_msg_type, period, WC_time, PC_Time, Action_Type, Option1, Option2, Option3,
#              Team_id, Person1, Person2, Person3, Team_id_type, Person1_type, Person2_type, Person3_type]
    #   Don't need game_id (0),Team_id(10), Team_id_type(14), Person1_type(15), Person2_type(16), Person3_type(17)









