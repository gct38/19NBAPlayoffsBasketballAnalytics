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