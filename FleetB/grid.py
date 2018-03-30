from configuration import GridConfig, GameRule

class Grid(object):
    def __init__(self):
        self.cells = [];
        self.init();

    def init(self):
        self.cells = [[0] * GameRule.MAX_OF_Y for i in range(GameRule.MAX_OF_X)]

    def isUndamagedShip(self, x, y):
        return self.cells[x][y] == GridConfig.TYPE_SHIP;

    def isMiss(self, x, y):
        return self.cells[x][y] == GridConfig.TYPE_MISS;

    def isDamagedShip(self, x, y):
        return self.cells[x][y] == GridConfig.TYPE_HIT or self.cells[x][y] == GridConfig.TYPE_SUNK;

    def updateCell(self, x, y, type_ship):
        self.cells[x][y] = type_ship

    def printGrid(self):
        for y in range(GameRule.MAX_OF_Y) :
            stri = ""
            for x in range(GameRule.MAX_OF_X) :
                stri += str(self.cells[x][y]) + "\t"
            print stri
           