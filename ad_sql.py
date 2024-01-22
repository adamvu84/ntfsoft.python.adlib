"""
Created on 27/05/2022 01:17

@author: Anh Duc
"""

import mysql.connector
import time
import configparser
from adlib import ad_utils as adu


_log = None


def get_connection(logger, config_file_path, section='sql'):
    init_logger(logger)
    return try_connect_sql(config_file_path, section)


def init_logger(logger=None):
    global _log
    if logger != None:
        _log = logger
    else:
        import logging
        _log = logging.getLogger()


def selectOne(conn, sql, params):
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        return cursor.fetchone()
    except mysql.connector.Error as ex:
        _log.exception(ex)
        _log.error(params)
        conn.rollback()
        return []
    finally:
        cursor.close()


def select(conn, sql, params):
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()
    except mysql.connector.Error as ex:
        _log.exception(ex)
        _log.error(params)
        conn.rollback()
        return []
    finally:
        cursor.close()


def execute(conn, sql, params, commit):
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        if commit:
            conn.commit()
    except mysql.connector.Error as ex:
        _log.exception(ex)
        _log.error(params)
        conn.rollback()
    finally:
        cursor.close()


def batch_execute(cursor, sql, params):
    try:
        cursor.execute(sql, params)
    except mysql.connector.Error as ex:
        _log.exception(ex)
        _log.error(params)


def callproc(conn, sql, params):
    try:
        cursor = conn.cursor(prepared=True)
        cursor.callproc(sql, params)
        conn.commit()
    except mysql.connector.Error as ex:
        _log.exception(ex)
        _log.error(params)
        conn.rollback()
    finally:
        cursor.close()


def read_sql_config(config_file_path, section):
    config_parser = configparser.RawConfigParser(allow_no_value=True)
    config_parser.read(config_file_path)
    return {
        'user': config_parser.get(section, 'user'),
        'password': config_parser.get(section, 'password'),
        'host': config_parser.get(section, 'host'),
        'port': config_parser.get(section, 'port'),
        'database': config_parser.get(section, 'database')
    }


def try_connect_sql(config_file_path, section='sql'):
    reconnect_ok = False
    reconnect_counter = 1

    try:
        sql_config = read_sql_config(config_file_path, section)
    except Exception as ex:
        s_err = 'Cannot read sql config exception'
        print(s_err)
        _log.exception(ex)
        return None

    while not reconnect_ok:
        try:
            conn = mysql.connector.connect(
                user=sql_config['user'],
                password=sql_config['password'],
                host=sql_config['host'],
                port=sql_config['port'],
                database=sql_config['database']
            )
            reconnect_ok = True
            return conn
        except Exception as ex:
            if reconnect_counter == 10:
                return None
            s_err = 'Cannot connect sql exception #{0} at {1}'
            print(s_err.format(reconnect_counter, adu.ad_datetime_str()))
            _log.exception(ex)
            reconnect_counter += 1
            time.sleep(70)
