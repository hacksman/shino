# coding: utf-8
# @Time : 9/8/21 9:52 AM

import sys
import time

import pymongo
from pymongo.errors import AutoReconnect


def auto_reconnect(retry_limit=30, retry_delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            tried_times = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except AutoReconnect:
                    tried_times += 1
                    if tried_times > retry_limit:
                        raise Exception(f"pymongo cannot reconnect successfully after {retry_limit} retries.")
                    time.sleep(retry_delay)

        return wrapper

    return decorator


class MongoExt:
    ASCENDING = pymongo.ASCENDING
    DESCENDING = pymongo.DESCENDING

    def __init__(self, dbhost, dbport, dbname, dbuser, dbpass, table):
        try:
            self.conn = pymongo.MongoClient(dbhost, dbport,
                                            connectTimeoutMS=30 * 60 * 1000,
                                            serverSelectionTimeoutMS=30 * 60 * 1000,
                                            maxPoolSize=600)
            self.db = self.conn[dbname]
            if dbuser and dbpass:
                self.connected = self.db.authenticate(dbuser, dbpass)
            else:
                self.connected = True

            self.collection = self.db[table]
        except Exception as e:
            sys.exit(1)

    def __del__(self):
        self.db.logout()
        self.conn.close()

    @auto_reconnect()
    def traverse_batch(self, where=None, sort=None, field=None, batch_size=500, limit=0):
        cursor = None
        try:
            where = {} if where is None else where
            if not sort:
                if field:
                    cursor = self.collection.find(where, field, no_cursor_timeout=True).batch_size(batch_size).limit(limit)
                else:
                    cursor = self.collection.find(where, no_cursor_timeout=True).batch_size(batch_size).limit(limit)
            else:
                if field:
                    cursor = self.collection.find(where, field, no_cursor_timeout=True).sort(sort).batch_size(batch_size).limit(
                        limit)
                else:
                    cursor = self.collection.find(where,no_cursor_timeout=True).sort(sort).batch_size(batch_size).limit(
                        limit)
            for item in cursor:
                yield item
        except Exception as e:
            raise e
        finally:
            if cursor is not None:
                cursor.close()

    @auto_reconnect()
    def update(self, spec, document, upsert=False, manipulate=False,
               multi=False, check_keys=True, **kwargs):
        self.collection.update(spec, document, upsert=upsert, multi=multi,
                               manipulate=manipulate, check_keys=check_keys,
                               **kwargs)

    @auto_reconnect()
    def update_one(self, filter, update, upsert=False,
                   bypass_document_validation=False):
        self.collection.update_one(filter, update, upsert=upsert,
                                   bypass_document_validation=bypass_document_validation)

    @auto_reconnect()
    def create_index(self, index, cache_for=300, **kwargs):
        self.collection.ensure_index(index, cache_for=cache_for, **kwargs)
