'''
    Properties:
    playerId = player's ID (string)
    defRtg = def rating for the season
    offRtg = off rating for the season
    possessions = # possessions player was active for in the game
    pointsScored = pts team scores with player on floor
    pointsAllowed = pts team allows with player on floor
'''
class Player:
    def __init__(self, playerId, teamId):
        self.playerId = str(playerId).strip()
        self.teamId = str(teamId).strip()
        self.active = False
        self.defRtg = 0
        self.offRtg = 0
        self.possessions = 0
        self.pointsAllowed = 0
        self.pointsScored = 0

    def calculateRtg(self):
        if self.possessions == 0:
            self.offRtg = 0
            self.defRtg = 0
        else:
            self.offRtg = self.pointsScored/self.possessions
            self.defRtg = self.pointsAllowed/self.possessions

    # + operator overload to add for pts scored
    def __add__(self, other):
        self.pointsScored += other
        self.possessions += 1

    # - operator overload to add for pts allowed
    def __sub__(self, other):
        self.pointsAllowed += other
        self.possessions += 1