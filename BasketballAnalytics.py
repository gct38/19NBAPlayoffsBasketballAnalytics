from parsers import parseEventCodes as parseEventCodes
from parsers import parseGameLineup as parseGameLineup
from parsers import parsePlayByPlay as parsePlayByPlay
from EventCodes import searchEventCodes as searchEventCodes
import csv


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
##  Notes:
#Use # of possessions to see if user is actually active in that game???
#       because you can rack up DNP-Coach's Decisions

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
    print()
    print()

        #testing Game, StartingLineup, Player, Rating class objects
    games = parseGameLineup("Game_Lineup.txt")
    parsePlayByPlay("Play_by_Play.txt", games)

    #TODO: Game.players property; what is Option3?
    print(len(games))
    print(games["006728e4c10e957011e1f24878e6054a"].gameId)
    print(games["006728e4c10e957011e1f24878e6054a"].teams)
    print(len(games["006728e4c10e957011e1f24878e6054a"].players))
    curr_game = games["006728e4c10e957011e1f24878e6054a"]
    curr_game.ratings()
    players = curr_game.players
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









