from configuration  import AiConfig, ShipConfig, GridConfig, TypeOfShip, GameRule

class Ship(object):
    sunk = False
    def __init__(self, ship_type, playerGrid):
        self.damage = 0
        self.ship_type = ship_type
        # self.points = points
        self.playerGrid = playerGrid;

        if ship_type == TypeOfShip.CARRIER:
            self.shipLength = 5
        elif ship_type == TypeOfShip.BATTLE_SHIP:
            self.shipLength = 4
        elif ship_type == TypeOfShip.OIL_RIG:
            self.shipLength = 4
        elif ship_type == TypeOfShip.CRUISER:
            self.shipLength = 3
        elif ship_type == TypeOfShip.DESTROYER:
            self.shipLength = 2

        self.maxDamage = self.shipLength
        self.suck = False

    def isLegal(self, x, y, direction, virtual):
        if self.ship_type == TypeOfShip.CARRIER :
            return self.isLegalCarrier(x, y, direction)
        elif self.ship_type == TypeOfShip.OIL_RIG :
            return self.isLegalOilRig(x, y, direction)
        elif self.withinBounds(x, y, direction) :
            for i in range(self.shipLength):
                if (direction == ShipConfig.DIRECTION_HORIZONTAL) :
                    if (self.playerGrid.cells[x + i][y] == GridConfig.TYPE_SHIP or
                        self.playerGrid.cells[x + i][y] == GridConfig.TYPE_MISS or
                        self.playerGrid.cells[x + i][y] == GridConfig.TYPE_SUNK) :
                        return False;
                else :
                    if (self.playerGrid.cells[x][y + i] == GridConfig.TYPE_SHIP or
                        self.playerGrid.cells[x][y + i] == GridConfig.TYPE_MISS or
                        self.playerGrid.cells[x][y + i] == GridConfig.TYPE_SUNK) :
                        return False;
            return True;
        else :
            return False;

    def isLegalCarrier(self, x, y, direction):
        if self.ship_type == TypeOfShip.CARRIER and self.withinBounds(x, y, direction) :
            if (direction == ShipConfig.DIRECTION_HORIZONTAL) :
                for i in range(self.shipLength - 1):
                    if (self.playerGrid.cells[x + i][y] == GridConfig.TYPE_SHIP or
                        self.playerGrid.cells[x + i][y] == GridConfig.TYPE_MISS or
                        self.playerGrid.cells[x + i][y] == GridConfig.TYPE_SUNK) :
                        return False;
                if (self.playerGrid.cells[x + 1][y - 1] == GridConfig.TYPE_SHIP or
                    self.playerGrid.cells[x + 1][y - 1] == GridConfig.TYPE_MISS or
                    self.playerGrid.cells[x + 1][y - 1] == GridConfig.TYPE_SUNK) :
                    return False;
            else :
                for i in range(self.shipLength - 1):
                    if (self.playerGrid.cells[x][y + i] == GridConfig.TYPE_SHIP or
                        self.playerGrid.cells[x][y + i] == GridConfig.TYPE_MISS or
                        self.playerGrid.cells[x][y + i] == GridConfig.TYPE_SUNK) :
                        return False;
                if (self.playerGrid.cells[x - 1][y + 1] == GridConfig.TYPE_SHIP or
                    self.playerGrid.cells[x - 1][y + 1] == GridConfig.TYPE_MISS or
                    self.playerGrid.cells[x - 1][y + 1] == GridConfig.TYPE_SUNK) :
                    return False;
            return True;
        else :
            return False;

    def isLegalOilRig(self, x, y, direction):
        if self.ship_type == TypeOfShip.OIL_RIG and self.withinBounds(x, y, direction) :
            if (direction == ShipConfig.DIRECTION_HORIZONTAL) :
                for i in range(self.shipLength - 2):
                    for j in range(self.shipLength - 2):
                        if (self.playerGrid.cells[x + i][y + j] == GridConfig.TYPE_SHIP or
                            self.playerGrid.cells[x + i][y + j] == GridConfig.TYPE_MISS or
                            self.playerGrid.cells[x + i][y + j] == GridConfig.TYPE_SUNK) :
                            return False;
            else :
                for i in range(self.shipLength - 2):
                    for j in range(self.shipLength - 2):
                        if (self.playerGrid.cells[x + i][y + j] == GridConfig.TYPE_SHIP or
                            self.playerGrid.cells[x + i][y + j] == GridConfig.TYPE_MISS or
                            self.playerGrid.cells[x + i][y + j] == GridConfig.TYPE_SUNK) :
                            return False;
            return True;
        else :
            return False;

    def create(self, x, y, direction, virtual):
        self.xPosition = x;
        self.yPosition = y;
        self.direction = direction;
        if (not virtual) :
            if self.ship_type == TypeOfShip.CARRIER:
                if (self.direction == ShipConfig.DIRECTION_HORIZONTAL) :
                    self.playerGrid.cells[x][y] = GridConfig.TYPE_SHIP;
                    self.playerGrid.cells[x + 1][y] = GridConfig.TYPE_SHIP;
                    self.playerGrid.cells[x + 2][y] = GridConfig.TYPE_SHIP;
                    self.playerGrid.cells[x + 3][y] = GridConfig.TYPE_SHIP;
                    self.playerGrid.cells[x + 1][y - 1] = GridConfig.TYPE_SHIP;
                else :
                    self.playerGrid.cells[x][y] = GridConfig.TYPE_SHIP;
                    self.playerGrid.cells[x][y + 1] = GridConfig.TYPE_SHIP;
                    self.playerGrid.cells[x][y + 2] = GridConfig.TYPE_SHIP;
                    self.playerGrid.cells[x][y + 3] = GridConfig.TYPE_SHIP;
                    self.playerGrid.cells[x - 1][y + 1] = GridConfig.TYPE_SHIP;
            elif self.ship_type == TypeOfShip.OIL_RIG:
                self.playerGrid.cells[x][y] = GridConfig.TYPE_SHIP;
                self.playerGrid.cells[x + 1][y] = GridConfig.TYPE_SHIP;
                self.playerGrid.cells[x][y + 1] = GridConfig.TYPE_SHIP;
                self.playerGrid.cells[x + 1][y + 1] = GridConfig.TYPE_SHIP;
            else :
                for i in range(self.shipLength):
                    if (self.direction == ShipConfig.DIRECTION_HORIZONTAL) :
                        self.playerGrid.cells[x + i][y] = GridConfig.TYPE_SHIP;
                    else :
                        self.playerGrid.cells[x][y + i] = GridConfig.TYPE_SHIP;

    def withinBounds(self, x, y, direction):
        if self.ship_type == TypeOfShip.CARRIER:
            if (direction == ShipConfig.DIRECTION_HORIZONTAL) :
                return y - 1 >= 0 and x + self.shipLength - 1 < GameRule.MAX_OF_X;
            else :
                return y + self.shipLength - 1 < GameRule.MAX_OF_Y and x - 1 > 0
        if self.ship_type == TypeOfShip.OIL_RIG:
            return x + 1 < GameRule.MAX_OF_X and y + 1 < GameRule.MAX_OF_Y ;

        if (direction == ShipConfig.DIRECTION_HORIZONTAL) :
            return x + self.shipLength < GameRule.MAX_OF_X;
        else :
            return y + self.shipLength < GameRule.MAX_OF_Y;

    def incrementDamage(self):
        self.damage += 1;
        if self.isSunk() :
            self.sinkShip(False);

    def isSunk(self):
        return self.damage >= self.maxDamage;

    def sinkShip(self, virtual):
        self.damage = self.maxDamage
        self.sunk = True
        if (not virtual) :
            allCells = self.getAllShipCells();
            for i in range(self.shipLength):
                self.playerGrid.updateCell(allCells[i][0], allCells[i][1], GridConfig.TYPE_SUNK);

    def getAllShipCells(self):
        resultObject = [];
        if self.ship_type == TypeOfShip.CARRIER:
            if (self.direction == ShipConfig.DIRECTION_HORIZONTAL) :
                resultObject.append([self.xPosition, self.yPosition]);
                resultObject.append([self.xPosition + 1, self.yPosition]);
                resultObject.append([self.xPosition + 2, self.yPosition]);
                resultObject.append([self.xPosition + 3, self.yPosition]);
                resultObject.append([self.xPosition + 1, self.yPosition - 1]);
            else :
                resultObject.append([self.xPosition, self.yPosition]);
                resultObject.append([self.xPosition, self.yPosition + 1]);
                resultObject.append([self.xPosition, self.yPosition + 2]);
                resultObject.append([self.xPosition, self.yPosition + 3]);
                resultObject.append([self.xPosition - 1, self.yPosition + 1]);
        elif self.ship_type == TypeOfShip.OIL_RIG:
            resultObject.append([self.xPosition, self.yPosition]);
            resultObject.append([self.xPosition, self.yPosition + 1]);
            resultObject.append([self.xPosition + 1, self.yPosition]);
            resultObject.append([self.xPosition + 1, self.yPosition + 1]);
        else :
            for i in range(self.shipLength):
                if (self.direction == ShipConfig.DIRECTION_HORIZONTAL) :
                    resultObject.append([self.xPosition + i, self.yPosition]);
                else :
                    resultObject.append([self.xPosition, self.yPosition + i]);
        return resultObject;
