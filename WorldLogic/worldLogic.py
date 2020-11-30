import random
from enum import Enum


class Directions(Enum):
    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"


class CellTypes(Enum):
    CITY = "C"
    LAND = "L"
    GLACIER = "G"
    FOREST = "F"
    SEA = "S"


Colors = {
    "C": "gray",
    "L": "brown",
    "G": "white",
    "F": "green",
    "S": "blue"
}

DIRECTIONS_LIST = [e.value for e in Directions]
CELL_TYPES_LIST = [e.value for e in CellTypes]

WORLD_SIZE = 25
CITY_POLLUTION = 0.1
FOREST_PURIFY = 0.2
MAX_POLLUTION = 1000
MIN_POLLUTION = 0
CITY_BURN = 60
FOREST_BURN = 40
GLACIER_MELT = 0
INIT_TEMP = 20
GLACIER_INIT_TEMP = -10
INIT_AIR_POLLUTION = 0
POLLUTION_WIND_MOVEMENT_PERCENT = 0.023
WIND_DIRECTIONS_NUM = 2
POLLUTION_TEMP_INCREASE_PERCENT = 0.00022

NEIGHBOUR_DEFICIT_EFFECT = 20


class Wind:
    def __init__(self):
        self.power = random.randint(1, 2)
        self.directions = random.sample(DIRECTIONS_LIST, WIND_DIRECTIONS_NUM)


class WorldCell:
    def __init__(self, cType, temp, wind, airPollution):
        self.cType = cType
        self.temp = temp
        self.wind = wind
        self.airPollution = airPollution

    def calcNextGen(self, n, e, s, w):
        nextType = self.cType
        nextWind = self.wind
        nextTemp = self.temp
        pollutionIncrement = 0

        nextTemp += POLLUTION_TEMP_INCREASE_PERCENT * self.airPollution

        if self.cType == CellTypes.CITY.value:
            pollutionIncrement += CITY_POLLUTION
            if self.temp >= CITY_BURN:
                nextType = CellTypes.LAND.value

        elif self.cType == CellTypes.FOREST.value:
            pollutionIncrement -= FOREST_PURIFY
            if self.temp >= FOREST_BURN:
                nextType = CellTypes.LAND.value
        elif self.cType == CellTypes.GLACIER.value and self.temp > GLACIER_MELT:
            nextType = CellTypes.SEA.value

        if Directions.SOUTH.value in n.wind.directions and n.airPollution > 0:
            pollutionIncrement += n.airPollution * n.wind.power * POLLUTION_WIND_MOVEMENT_PERCENT

        if Directions.WEST.value in e.wind.directions and e.airPollution > 0:
            pollutionIncrement += e.airPollution * e.wind.power * POLLUTION_WIND_MOVEMENT_PERCENT

        if Directions.NORTH.value in s.wind.directions and s.airPollution > 0:
            pollutionIncrement += s.airPollution * s.wind.power * POLLUTION_WIND_MOVEMENT_PERCENT

        if Directions.EAST.value in w.wind.directions and w.airPollution > 0:
            pollutionIncrement += w.airPollution * w.wind.power * POLLUTION_WIND_MOVEMENT_PERCENT

        neighbListTemp = [w.temp, s.temp, n.temp, e.temp]
        neighAvg = sum(neighbListTemp) / len(neighbListTemp)
        if neighAvg - NEIGHBOUR_DEFICIT_EFFECT > self.temp:
            nextTemp += 1

        if self.airPollution > MIN_POLLUTION:
            pollutionIncrement -= self.airPollution * POLLUTION_WIND_MOVEMENT_PERCENT * WIND_DIRECTIONS_NUM
        if pollutionIncrement > 0:
            nextAirPollution = min(MAX_POLLUTION, self.airPollution + pollutionIncrement)
        else:
            nextAirPollution = max(MIN_POLLUTION, self.airPollution + pollutionIncrement)

        nextGen = WorldCell(nextType, nextTemp, nextWind, nextAirPollution)
        return nextGen


class World:
    def __init__(self):
        self.genNum = 0
        self.currGen = self.loadWorld()

    def loadWorld(self):
        loadedWorld = [[0] * WORLD_SIZE for i in range(WORLD_SIZE)]
        file = open("smallworld.txt", "r")

        for r in range(0, WORLD_SIZE):
            currRow = file.readline()
            for c in range(0, WORLD_SIZE):
                cType = currRow[c]

                if cType not in CELL_TYPES_LIST:
                    if cType == '\n':
                        continue
                    else:
                        raise Exception("World file is not valid")

                randomWind = Wind()
                temp = INIT_TEMP if cType != CellTypes.GLACIER.value else GLACIER_INIT_TEMP
                airPollution = INIT_AIR_POLLUTION
                loadedWorld[r][c] = WorldCell(cType, temp, randomWind, airPollution)

        return loadedWorld

    def calcNextGen(self):
        nextGen = [[0] * WORLD_SIZE for i in range(WORLD_SIZE)]

        for r in range(0, WORLD_SIZE):
            for c in range(0, WORLD_SIZE):
                n = self.currGen[(r - 1) % WORLD_SIZE][c]
                s = self.currGen[(r + 1) % WORLD_SIZE][c]
                e = self.currGen[r][(c + 1) % WORLD_SIZE]
                w = self.currGen[r][(c - 1) % WORLD_SIZE]
                currCell = self.currGen[r][c]
                cellNextGen = currCell.calcNextGen(n, e, s, w)
                nextGen[r][c] = cellNextGen

        self.currGen = nextGen
        self.genNum += 1
