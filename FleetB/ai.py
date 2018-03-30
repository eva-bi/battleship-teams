from configuration import AiConfig, GameRule, ShipConfig, GridConfig, TypeOfShip
from grid import Grid
from fleet import Fleet
from ship import Ship
from random import randint, random, sample
import numpy as np
from user import *
from helper import Helper
import time
class AI(object):

    def __init__(self, ships):
        self.virtualGrid = Grid();
        self.virtualFleet = Fleet(ships);

        self.probGrid = [];
        self.initProbs();
        self.updateProbs();

    def shoot(self, maxShots):
        if maxShots == 2 and len(self.virtualFleet.fleetRoster) == 1:
            first_shot = self.shoot_basic()

            temp_virtualGrid = [[0] * GameRule.MAX_OF_Y for i in range(GameRule.MAX_OF_X)]
            temp_virtualGrid = self.virtualGrid.cells

            self.virtualGrid.cells[first_shot[0]][first_shot[1]] = GridConfig.TYPE_HIT;
            self.updateProbs();
            second_shot = self.shoot_basic()

            self.virtualGrid.cells = temp_virtualGrid
            return [first_shot, second_shot]
        if maxShots >= 3 :
            first_shot = self.shoot_basic()

            temp_virtualGrid = [[0] * GameRule.MAX_OF_Y for i in range(GameRule.MAX_OF_X)]
            temp_virtualGrid = self.virtualGrid.cells

            self.virtualGrid.cells[first_shot[0]][first_shot[1]] = GridConfig.TYPE_HIT;
            self.updateProbs();
            second_shot = self.shoot_basic()

            self.virtualGrid.cells[first_shot[0]][first_shot[1]] = GridConfig.TYPE_MISS;
            self.updateProbs();
            third_shot = self.shoot_basic()

            self.virtualGrid.cells = temp_virtualGrid
            return [first_shot, second_shot, third_shot]
        else:
            return [self.shoot_basic()]

    def shoot_basic(self):
        maxProbability = 0;
        maxProbCoords = [];
        maxProbs = [];
        ai_queue = [];

        # add behavier of user
        # ships = CV_MAP + BB_MAP + OR_MAP + CA_MAP + DD_MAP
        # for ship in ships:
        #    for cell in ship:
        #        if (self.probGrid[cell[0]][cell[1]] != 0) :
        #            self.probGrid[cell[0]][cell[1]] += 1;

        #for i in range(len(AiConfig.OPENINGS)) :
        #    cell = AiConfig.OPENINGS[i];
        #     if (self.probGrid[cell['x']][cell['y']] != 0) :
        #        self.probGrid[cell['x']][cell['y']] += int(cell['weight']);

        for x in range(GameRule.MAX_OF_X) :
            for y in range(GameRule.MAX_OF_Y) :
                if (self.probGrid[x][y] > maxProbability) :
                    maxProbability = self.probGrid[x][y];
                    maxProbs = [[x, y]];
                elif (self.probGrid[x][y] == maxProbability) :
                    maxProbs.append([x, y]);
        if random() < AiConfig.RANDOMNESS :
            # maxProbCoords = maxProbs[randint(0, len(maxProbs) - 1)]
            maxProbCoords = sample(maxProbs, 1)[0]
        else :
            maxProbCoords = maxProbs[0];
        return maxProbCoords

    def updateProbs(self):
        roster = self.virtualFleet.fleetRoster;
        coords = [];
        self.resetProbs();

        for k in range(len(roster)) :
            for x in range(GameRule.MAX_OF_X) :
                for y in range(GameRule.MAX_OF_Y) :
                    if (roster[k].isLegal(x, y, ShipConfig.DIRECTION_HORIZONTAL, 1)) :
                        roster[k].create(x, y, ShipConfig.DIRECTION_HORIZONTAL, True);
                        coords = roster[k].getAllShipCells();
                        if (self.passesThroughHitCell(coords)) :
                            for i in range(len(coords)) :
                                self.probGrid[coords[i][0]][coords[i][1]] += AiConfig.PROB_WEIGHT * self.numHitCellsCovered(coords);
                        else :
                            for _i in range(len(coords)) :
                                self.probGrid[coords[_i][0]][coords[_i][1]] += 1;

                    if (roster[k].isLegal(x, y, ShipConfig.DIRECTION_VERTICAL, 1)) :
                        roster[k].create(x, y, ShipConfig.DIRECTION_VERTICAL, True);
                        coords = roster[k].getAllShipCells();
                        if (self.passesThroughHitCell(coords)) :
                            for j in range(len(coords)) :
                                self.probGrid[coords[j][0]][coords[j][1]] += AiConfig.PROB_WEIGHT * self.numHitCellsCovered(coords);
                        else :
                            for _j in range(len(coords)) :
                                self.probGrid[coords[_j][0]][coords[_j][1]] += 1;

                    if (self.virtualGrid.cells[x][y] == GridConfig.TYPE_HIT) :
                        self.probGrid[x][y] = 0;


    def initProbs(self) :
        self.probGrid = [[0] * GameRule.MAX_OF_Y for i in range(GameRule.MAX_OF_X)]

    def resetProbs(self) :
        self.probGrid = [[0] * GameRule.MAX_OF_Y for i in range(GameRule.MAX_OF_X)]

    def passesThroughHitCell(self, shipCells) :
        for cellShip in shipCells :
            if (self.virtualGrid.cells[cellShip[0]][cellShip[1]] == GridConfig.TYPE_HIT) :
                return True;
        return False;

    def numHitCellsCovered(self, shipCells) :
        cells = 0;
        for i in range(len(shipCells)) :
            if (self.virtualGrid.cells[shipCells[i][0]][shipCells[i][1]] == GridConfig.TYPE_HIT) :
                cells += 1;
        return cells;

    # for game engine
    def findHumanShip(self, x, y) :
        return self.humanFleet.findShipByCoords(x, y);