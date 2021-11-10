# coding: utf-8
# @Time : 2020/12/7 9:01 AM

import datetime
from dbutils.pooled_db import PooledDB
import pymysql


class MysqlExt:
    __pool_map = {}
    __pool = None

    def __init__(self, host, port,
                 db, user, password,
                 mincached=2, maxcached=12, maxshared=10, maxconnections=100, blocking=True,
                 maxusage=10, setsession=["set autocommit = 1"], reset=True, charset='utf8mb4'
                 ):
        if not self.__pool_map.get((host, port, db, user, password)):
            self.__class__.__pool = PooledDB(pymysql,
                                             mincached, maxcached,
                                             maxshared, maxconnections, blocking,
                                             maxusage, setsession, reset,
                                             host=host, port=port, db=db,
                                             user=user, passwd=password,
                                             charset=charset,
                                             cursorclass=pymysql.cursors.DictCursor
                                             )
            self.__class__.__pool_map[(host, port, db, user, password)] = self.__class__.__pool
        else:
            self.__class__.__pool = self.__class__.__pool_map.get((host, port, db, user, password))

        self._conn = None
        self._cursor = None
        self.__get_conn()

    def __get_conn(self):
        self._conn = self.__pool.connection()
        self._cursor = self._conn.cursor()

    def close(self):
        try:
            self._cursor.close()
            self._conn.close()
        except Exception as e:
            print(e)

    @staticmethod
    def __dict_datetime_obj_to_str(result_dict):
        if result_dict:
            result_replace = {k: v.__str__() for k, v in result_dict.items() if isinstance(v, datetime.datetime)}
            result_dict.update(result_replace)
        return result_dict

    def select_one(self, sql: str, param: set = ()) -> None or dict:
        self.execute(sql, param)
        result = self._cursor.fetchone()
        result = self.__dict_datetime_obj_to_str(result)
        return result

    def select_many(self, sql: str, param: set = ()) -> iter:
        self.execute(sql, param)
        for item in self._cursor._cursor:
            item = self.__dict_datetime_obj_to_str(item)
            yield item

    def execute(self, sql: str, param: set = ()) -> int:
        count = self._cursor.execute(sql, param)
        return count

    def execute_many(self, sql: str, params: list) -> int:
        count = self._cursor.executemany(sql, params)
        return count

    def begin(self):
        self._conn.begin()

    def end(self, succeed=True):
        if succeed:
            self._conn.commit()
        else:
            self._conn.rollback()
