"""
Created on 27/05/2022 01:17

@author: Anh Duc
"""

import redis
import configparser
from adlib import ad_utils as adu


_log = None


def get_connection(logger, config_file_path):
    init_logger(logger)
    return try_connect_redis(config_file_path)


def init_logger(logger=None):
    global _log
    if logger != None:
        _log = logger
    else:
        import logging
        _log = logging.getLogger()


def read_redis_config(config_file_path):
    config_parser = configparser.RawConfigParser(allow_no_value=True)
    config_parser.read(config_file_path)
    return {
        'host': config_parser.get('redis', 'host'),
        'port': config_parser.get('redis', 'port'),
    }


def try_connect_redis(config_file_path):
    reconnect_ok = False
    reconnect_counter = 1
    while not reconnect_ok:
        try:
            redis_config = read_redis_config(config_file_path)
            conn = redis.Redis(host=redis_config['host'], port=redis_config['port'], decode_responses=True)
            conn.ping()
            reconnect_ok = True
            return conn
        except Exception as ex:
            if reconnect_counter == 10:
                return None
            s_err = 'Cannot connect redis exception #{0} at {1}'
            print(s_err.format(reconnect_counter, adu.ad_datetime_str()))
            _log.exception(ex)
            reconnect_counter += 1
            time.sleep(15)
