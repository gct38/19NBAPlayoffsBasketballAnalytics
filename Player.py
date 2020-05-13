'''
    Properties:
    playerId = player's ID (string)
    defRtg = def rating for the game
    offRtg = off rating for the game
    possessions = # possessions player was active for in the game
    pointsScored = pts team scores with player on floor
    pointsAllowed = pts team allows with player on floor
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