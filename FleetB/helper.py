import cPickle
import random
import numpy as np
from flask import jsonify
from configuration import CacheConfig, TypeOfShip, GameRule

class Helper(object):
    @staticmethod
    def get_robot_info_key(session_id):
        return CacheConfig.ROBOT_PREFIX + session_id

    @staticmethod
    def get_human_fleet_info_key(session_id):
        return CacheConfig.HUMAN_FLEET_PREFIX + session_id

    @staticmethod
    def get_ai_fleet_info_key(session_id):
        return CacheConfig.AI_FLEET_PREFIX + session_id

    @staticmethod
    def get_ship_info_key(session_id):
        return CacheConfig.SHIP_INFO_PREFIX + session_id

    @staticmethod
    def get_shots_info_key(session_id):
        return CacheConfig.SHOT_INFO_PREFIX + session_id

    @staticmethod
    def get_bot_session_id(request):
        return request.headers.get('X-Session-Id') + GameRule.BOT_ID

    @staticmethod
    def get_session_id(request):
        return request.headers.get('X-Session-Id')

    @staticmethod
    def get_token_id(request):
        return request.headers.get('X-token')

    @staticmethod
    def get_cache(redis, key):
        if redis.get(key) :
            return cPickle.loads(redis.get(key))
        else :
            return "";

    @staticmethod
    def cache_info(redis, key, value):
        redis.set(key, cPickle.dumps(value))

    @staticmethod
    def del_cache_info(redis, key):
        redis.delete(key)

    @staticmethod
    def response_to_invitation():
        return jsonify(
            {
               'success': True
            }
        )

    @staticmethod
    def response_to_start(ships):
        return jsonify(
            {
                'ships': ships
            }
        )

    @staticmethod
    def response_to_turn(coordinates):
        return jsonify(
            {
                'coordinates': coordinates
            }
        )

    @staticmethod
    def response_to_notification():
        return jsonify(
            {
                'success': True
            }
        )

    @staticmethod
    def response_unsuccess(msg):
        return jsonify(
            {
                'success': False,
                'info': msg
            }
        )
