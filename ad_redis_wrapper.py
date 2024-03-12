"""
Created on 27/05/2022 01:17

@author: Anh Duc
"""

import redis
import logging
import time


logger = logging.getLogger(__name__)

class RedisWrapper:
    def __init__(self, host, port, password = None, prefix = ''):
        self._host = host
        self._port = port
        self._password = password
        self._prefix = prefix
        self._conn = self._connect()

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()

    def _connect(self):
        reconnect_counter = 1
        while True:
            try:
                if self._password is None:
                    conn = redis.Redis(host=self._host, port=self._port, decode_responses=True)
                else:
                    conn = redis.Redis(host=self._host, port=self._port, password=self._password, decode_responses=True)
                conn.ping()
                return conn
            except Exception as ex:
                if reconnect_counter == 5:
                    raise Exception('Cannot connect to redis')
                logger.exception(ex)
                reconnect_counter += 1
                time.sleep(2)

    @property
    def connection(self):
        return self._conn

    def set(self, key, value):
        if self._prefix != '':
            self._conn.set(f"{self._prefix}:{key}", value)
        else:
            self._conn.set(key, value)

    def get(self, key):
        if self._prefix != '':
            return self._conn.get(f"{self._prefix}:{key}")
        else:
            return self._conn.get(key)

    def publish(self, channel, message):
        self._conn.publish(channel, message)