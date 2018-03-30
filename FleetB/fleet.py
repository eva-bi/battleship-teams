from ship import Ship
from grid import Grid
from configuration import AiConfig, ShipConfig, GameRule, TypeOfShip
import random
import numpy as np
import time
class Fleet(object):
    def __init__(self, ships):
        self.numShips = 0;
        self.playerGrid = Grid();
        self.ships = ships;
        self.fleetRoster = [];
        self.populate();

    def populate(self):
        for type in self.ships:
            self.fleetRoster.append(Ship(type, self.playerGrid));


    def placeShipsRandomly(self):
        # retry put ships into grid if all ships cant put
        while self.numShips != len(self.fleetRoster):
            self.playerGrid.init()
            self.doPlaceShipsRandomly()
            time.sleep(0.5)

    def doPlaceShipsRandomly(self):
        shipCoords = [];
        self.numShips = 0
        retry = 0
        for i in range(len(self.fleetRoster)):
            illegalPlacement = True;
            shipTypes = self.fleetRoster[i].ship_type;

            while (illegalPlacement and retry < 160) :
                retry += 1
                randomX = random.randint(0, GameRule.MAX_OF_X - 1);
                randomY = random.randint(0, GameRule.MAX_OF_Y - 1)
                randomDirection = random.randint(0, 1)
                if (self.fleetRoster[i].isLegal(randomX, randomY, randomDirection, 0)) :
                    self.fleetRoster[i].create(randomX, randomY, randomDirection, False);
                    shipCoords = self.fleetRoster[i].getAllShipCells();
                    self.numShips += 1
                    illegalPlacement = False;
                else :
                    continue;
                time.sleep(0.5)

    def findShipByCoords(self, x, y):
        for currentShip in self.fleetRoster:
            allCells = currentShip.getAllShipCells();
            for cellOfShip in allCells:
                if cellOfShip[0] == x and cellOfShip[1] == y:
                    return currentShip;


    def getAllFleetCells(self):
        ships = []
        for roster in self.fleetRoster:
            ship = {
                'coordinates': roster.getAllShipCells(),
                'type': roster.ship_type
            }
            ships.append(ship);
        return ships;

    def allShipsSunk(self):
        for i in range(len(self.fleetRoster)):
            if (self.fleetRoster[i].sunk == False) :
                return False;
        return True;


    def countShipsSunk(self):
        count = 0;
        for i in range(len(self.fleetRoster)):
            if (self.fleetRoster[i].sunk == True) :
                count += 1;
        return count;
