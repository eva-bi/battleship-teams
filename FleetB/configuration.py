from random import randint

class TypeOfShip(object):
    CARRIER = 'CV'
    BATTLE_SHIP = 'BB'
    OIL_RIG = 'OR'
    CRUISER = 'CA'
    DESTROYER = 'DD'


class GameRule(object):
    MAX_OF_X = 20
    MAX_OF_Y = 8
    HIT = "HIT"
    MISS = "MISS"
    PLAYER_ID = 'fleet_b'

class CacheConfig(object):
    SHIP_INFO_PREFIX = 'ship_info_'
    HUMAN_FLEET_PREFIX = 'humanfleet_'
    AI_FLEET_PREFIX = 'aifleet_'
    ROBOT_PREFIX = 'robot_'

class GridConfig(object):
    TYPE_EMPTY = 0 # 0 = water (empty)
    TYPE_SHIP = 1 # 1 = undamaged ship
    TYPE_MISS = 2 # 2 = water with a cannonball in it (missed shot)
    TYPE_HIT = 3 # 3 = damaged ship (hit shot)
    TYPE_SUNK = 4 # 4 = sunk ship

class ShipConfig(object):
    DIRECTION_VERTICAL = 0;
    DIRECTION_HORIZONTAL = 1;


class AiConfig(object):
    PROB_WEIGHT = 100;
    SHOT_HIGH_MIN = 20;
    SHOT_HIGH_MAX = 30;
    SHOT_MED_MIN = 15;
    SHOT_MED_MAX = 25;
    SHOT_LOW_MIN = 10;
    SHOT_LOW_MAX = 20;
    RANDOMNESS = 0.1;
    SHOTINGS = [
        {'x': 3, 'y': 0, 'weight': randint(SHOT_LOW_MIN, SHOT_LOW_MAX)},
        {'x': 7, 'y': 0, 'weight': randint(SHOT_LOW_MIN, SHOT_LOW_MAX)},
        {'x': 11, 'y': 0, 'weight': randint(SHOT_LOW_MIN, SHOT_LOW_MAX)},
        {'x': 15, 'y': 0, 'weight': randint(SHOT_LOW_MIN, SHOT_LOW_MAX)},
        {'x': 3, 'y': 9, 'weight': randint(SHOT_LOW_MIN, SHOT_LOW_MAX)},
        {'x': 7, 'y': 9, 'weight': randint(SHOT_LOW_MIN, SHOT_LOW_MAX)},
        {'x': 11, 'y': 9, 'weight': randint(SHOT_LOW_MIN, SHOT_LOW_MAX)},
        {'x': 15, 'y': 9, 'weight': randint(SHOT_LOW_MIN, SHOT_LOW_MAX)},
        {'x': 0, 'y': 3, 'weight': randint(SHOT_MED_MIN, SHOT_MED_MAX)},
        {'x': 5, 'y': 3, 'weight': randint(SHOT_MED_MIN, SHOT_MED_MAX)},
        {'x': 9, 'y': 3, 'weight': randint(SHOT_MED_MIN, SHOT_MED_MAX)},
        {'x': 13, 'y': 3, 'weight': randint(SHOT_MED_MIN, SHOT_MED_MAX)},
        {'x': 19, 'y': 3, 'weight': randint(SHOT_MED_MIN, SHOT_MED_MAX)},
        {'x': 0, 'y': 0, 'weight': randint(SHOT_HIGH_MIN, SHOT_HIGH_MAX)},
        {'x': 0, 'y': 7, 'weight': randint(SHOT_HIGH_MIN, SHOT_HIGH_MAX)},
        {'x': 19, 'y': 0, 'weight': randint(SHOT_HIGH_MIN, SHOT_HIGH_MAX)},
        {'x': 19, 'y': 7, 'weight': randint(SHOT_HIGH_MIN, SHOT_HIGH_MAX)}
    ];
