import redis
from flask import Flask, request, jsonify
from fleet import Fleet
from ai import AI
from helper import Helper
from configuration import GameRule, GridConfig

app = Flask(__name__)
db = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    return "It's not personal. It's just bussiness"


@app.route('/invite', methods=['POST'])
def invite():
    print "================================================="
    session_id = Helper.get_session_id(request)
    info_ships = request.json.get('ships')
    boardWidth = request.json.get('boardWidth')
    boardHeight = request.json.get('boardHeight')
    if boardWidth != GameRule.MAX_OF_X and boardHeight != GameRule.MAX_OF_Y :
        return Helper.response_unsuccess("The board game is not 8 x 20 grids! Please check again!")

    if not info_ships :
        return Helper.response_unsuccess("There are not ships information! Please check again!")

    ships = [];
    for ship in info_ships:
        for i in range(0, int(ship['quantity'])):
            ships.append(ship['type']);
    print "Ships: ", ships
    # cache ship's information and delete fleet of human
    Helper.cache_info(db, Helper.get_ship_info_key(session_id), ships)
    Helper.del_cache_info(db, Helper.get_human_fleet_info_key(session_id))
    Helper.del_cache_info(db, Helper.get_ai_fleet_info_key(session_id))
    Helper.del_cache_info(db, Helper.get_robot_info_key(session_id))
    return Helper.response_to_invitation()


@app.route('/place-ships', methods=['POST'])
def place_ships():
    print "================================================="
    session_id = Helper.get_session_id(request)

    player_1 = request.json.get('player1')
    player_2 = request.json.get('player2')

    # get ships information from cache to do strategy
    ships = Helper.get_cache(db, Helper.get_ship_info_key(session_id))

    aiFleet = Helper.get_cache(db, Helper.get_ai_fleet_info_key(session_id))
    if not aiFleet:
        aiFleet = Fleet(ships);
        aiFleet.placeShipsRandomly();
        Helper.cache_info(db, Helper.get_ai_fleet_info_key(session_id), aiFleet)
    placed_ships = aiFleet.getAllFleetCells();
    #init robot
    robot = AI(ships);
    Helper.cache_info(db, Helper.get_robot_info_key(session_id), robot)
    return Helper.response_to_start(placed_ships)

@app.route('/shoot', methods=['POST'])
def shoot():
    print "===================== shoot ============================"
    session_id = Helper.get_session_id(request)
    turn = request.json.get('turn')
    maxShots = request.json.get('maxShots')
    # get robot
    robot = Helper.get_cache(db, Helper.get_robot_info_key(session_id))

    coordinates = robot.shoot(maxShots)
    # store robot
    Helper.cache_info(db, Helper.get_robot_info_key(session_id), robot)
    return Helper.response_to_turn(coordinates)

@app.route('/notify', methods=['POST'])
def notify():
    print "====================== notify ==========================="
    session_id = Helper.get_session_id(request)
    player_id = request.json.get('playerId')
    shots = request.json.get('shots')
    sunkShips = request.json.get('sunkShips')
    robot = Helper.get_cache(db, Helper.get_robot_info_key(session_id))
    if player_id == GameRule.PLAYER_ID:
        for shot in shots :
            coordinate = shot["coordinate"]
            status = shot["status"]
            if status == GameRule.HIT:
                robot.virtualGrid.cells[coordinate[0]][coordinate[1]] = GridConfig.TYPE_HIT;
            elif status == GameRule.MISS:
                robot.virtualGrid.cells[coordinate[0]][coordinate[1]] = GridConfig.TYPE_MISS;
        if sunkShips :
            for ship in sunkShips :
                for k in range(len(robot.virtualFleet.fleetRoster)) :
                    if ship['type'] == robot.virtualFleet.fleetRoster[k].ship_type :
                        robot.virtualFleet.fleetRoster.pop(k)
                        break;
                for cellOfShip in ship['coordinates']:
                    robot.virtualGrid.cells[cellOfShip[0] ][cellOfShip[1]] = GridConfig.TYPE_SUNK;
    # store robot
    robot.updateProbs();
    # store map status
    Helper.cache_info(db, Helper.get_robot_info_key(session_id), robot)
    return Helper.response_to_notification()

@app.route('/game-over', methods=['POST'])
def game_over():
    session_id = Helper.get_session_id(request)
    Helper.del_cache_info(db, Helper.get_ship_info_key(session_id))
    Helper.del_cache_info(db, Helper.get_human_fleet_info_key(session_id))
    Helper.del_cache_info(db, Helper.get_ai_fleet_info_key(session_id))
    Helper.del_cache_info(db, Helper.get_robot_info_key(session_id))
    # store ships of ememy into redis for next game
    # ........
    return Helper.response_to_notification()

@app.after_request
def apply_caching(response):
    session_id = Helper.get_session_id(request)
    token_id = Helper.get_token_id(request)
    response.headers["X-SESSION-ID"] = session_id
    response.headers["X-TOKEN"] = token_id
    return response
    
if __name__ == '__main__':
    print 'AI running !!!'
    app.run(host='0.0.0.0', port=8088, debug=True)
