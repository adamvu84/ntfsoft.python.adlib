"""
Created on 27/05/2022 01:17

@author: Anh Duc
"""

import mysql.connector
import time
import logging


logger = logging.getLogger(__name__)

class DatabaseWrapper:

    def __init__(self, host_name, port, user_name, password, database, charset, commit, prefix):
        self._conn = mysql.connector.connect(
            host=host_name,
            port=port,
            user=user_name,
            password=password,
            database=database,
            charset=charset,
            autocommit=commit)
        self._cursor = self._conn.cursor()
        self._prefix = prefix

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    @property
    def prefix(self):
        return self._prefix

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        try:
            self.cursor.execute(sql, params or ())
        except Exception as e:
            logger.exception(e)

    def executemany(self, sql, params=None):
        try:
            self.cursor.executemany(sql, params or ())
        except Exception as e:
            logger.exception(e)

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        try:
            self.cursor.execute(sql, params or ())
            return self.fetchall()
        except Exception as e:
            logger.exception(e)
            return None

    def queryOne(self, sql, params=None):
        try:
            self.cursor.execute(sql, params or ())
            return self.fetchone()
        except Exception as e:
            logger.exception(e)
            return None
