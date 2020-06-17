from EventCodes import searchEventCodes
from Game import parseGameLineup

import Player
#TODO: fact check make sure output data is correct
# cross list with potentially..? https://www.basketball-reference.com/playoffs/NBA_2018_per_poss.html

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


def output(games):
    file = open('Off_Def_Ratings_2018_Playoffs.csv', 'w')
    file.write("Game_ID, Player_ID, OffRtg, DefRtg\n")
    for game in games:
        games[game].ratings()
        for player in games[game].players:
            if games[game].players[player].possessions != 0:
                file.write(game + ',' + games[game].players[player].playerId + ',' + games[game].players[player].offRtg + ',' + games[game].players[player].defRtg + '\n')
    file.close()
    print("move complete")

#TODO: implement test scripts
#gets each player's total off/def ratings for the whole playoffs to help verify output data
def playoff_totals(games):
    allPlayers = dict()
    for game in games:
        games[game].ratings()
        for player in games[game].players:
            if games[game].players[player].possessions != 0:
                if games[game].players[player].playerId not in allPlayers:
                    allPlayers[games[game].players[player].playerId] = Player.Player(games[game].players[player].playerId, games[game].players[player].teamId)
                    allPlayers[games[game].players[player].playerId].possessions = games[game].players[player].possessions
                    allPlayers[games[game].players[player].playerId].pointsAllowed = games[game].players[player].pointsAllowed
                    allPlayers[games[game].players[player].playerId].pointsScored = games[game].players[player].pointsScored
                else:
                    allPlayers[games[game].players[player].playerId].possessions += games[game].players[player].possessions
                    allPlayers[games[game].players[player].playerId].pointsAllowed += games[game].players[player].pointsAllowed
                    allPlayers[games[game].players[player].playerId].pointsScored += games[game].players[player].pointsScored

    file = open('TEST_Total_Off_Def_Ratings_2018_Playoffs.csv', 'w')
    file.write("Player_ID, OffRtg, DefRtg\n")
    for player in allPlayers:
        allPlayers[player].calculateRtg()
        file.write(allPlayers[player].playerId + ',' + str(allPlayers[player].offRtg) + ',' + str(allPlayers[player].defRtg) + '\n')
    file.close()



#gets pt totals for all games to help verify output data
def game_scores(games):
    file = open('TEST_Game_Scores_2018_Playoffs.csv', 'w')
    file.write("Game_ID, Team1, Team1Pts, Team2, Team2Pts\n")
    for game in games:
        team1 = games[game].teams[0]
        team1pts = 0
        team2 = games[game].teams[1]
        team2pts = 0
        for player in games[game].players:
            if games[game].players[player].teamId == team1 and games[game].players[player].possessions != 0:
                team1pts += games[game].players[player].pointsScored
                team2pts += games[game].players[player].pointsAllowed
        file.write(game + ',' + team1 + ',' + str(team1pts/5) + ',' + team2 + ',' + str(team2pts/5) + '\n')
    file.close()


def test_scripts(games):
    playoff_totals(games)
    game_scores(games)



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

    output(games)
    test_scripts(games)
    print('done')


    '''
    #TODO: Game.players property; what is Option3?
    print(len(games))
    print(games["006728e4c10e957011e1f24878e6054a"].gameId)
    print(games["006728e4c10e957011e1f24878e6054a"].teams)
    print(len(games["006728e4c10e957011e1f24878e6054a"].players))
    curr_game = games["006728e4c10e957011e1f24878e6054a"]

    
    counter = 0
    for game in games:
        teams = dict()
        for play in games[game].play:
            if int(play['Event_Msg_Type']) == 8 and int(play['Period']) == 1:
                player = play['Person1']
                if games[game].players[player].teamId not in teams:
                    teams[games[game].players[player].teamId] = 1
                else:
                    teams[games[game].players[player].teamId] += 1
        for team in teams:
            if teams[team] < 5:
                print(games[game].gameId, team)
                counter += 1

    print(counter)


    removes = []
    for value in curr_game.play:
        if int(value['Event_Msg_Type']) != 8:
            removes.append(value)

    for value in removes:
        curr_game.play.remove(value)
    '''

    #curr_game.ratings()
    #players = curr_game.players
    #a = curr_game.helper()
    #print(a)
    #print(curr_game.players)
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









