# coding: utf-8
# @Time : 9/30/21 9:54 AM
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(script_dir))

from conf import PropertiesCenter, GlobalSetting

import argparse
import pymysql

parser = argparse.ArgumentParser()

parser.add_argument("--env",
                    choices=["debug", "local", "dev", "prod", "local_to_dev", "local_to_prod"],
                    help="set env[debug、local、dev、prod、local_to_dev、local_to_prod]"
                    )

args = parser.parse_args()

if not args.env:
    raise Exception(f"u must set env args for config")

GlobalSetting.env(args.env)

import sys
import traceback

from amqp.exceptions import AccessRefused, NotAllowed
from kombu import exceptions as kb_exp

import redis
from redis.exceptions import ConnectionError, TimeoutError, ResponseError
from glom import glom, PathAccessError
from pymysql import OperationalError

from shino.libs.log_ext import LogExt
from shino.libs.mysql_ext import MysqlExt
from shino.libs.rabbitmq_ext import RabbitmqExt

log = LogExt('db_check.log').get_logger

db_conf = PropertiesCenter._DB_SETTING


def db_is_ok():
    # create db if not exists
    cnx = pymysql.connect(host=PropertiesCenter.get_db('mysql.host'),
                          port=PropertiesCenter.get_db('mysql.port'),
                          user=PropertiesCenter.get_db('mysql.user'),
                          password=PropertiesCenter.get_db('mysql.password'))
    try:
        cursor = cnx.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {PropertiesCenter.get_db('mysql.db')}")
    except Exception as e:
        log.error(f"⚠️ Create mysql db failed:")
        for e_info in traceback.format_exception(*sys.exc_info()):
            for _ in e_info[:-1].split("\n"):
                log.error(_)
    finally:
        cnx.close()

    try:
        MysqlExt(**glom(db_conf, 'mysql'))
    except OperationalError:
        log.error(f"⚠️ Mysql connect failed:")
        for e_info in traceback.format_exception(*sys.exc_info()):
            for _ in e_info[:-1].split("\n"):
                log.error(_)
    except PathAccessError:
        log.error(f"⚠️ Parse db conf failed:")
        for e_info in traceback.format_exception(*sys.exc_info()):
            for _ in e_info[:-1].split("\n"):
                log.error(_)
    except Exception:
        log.error(f"⚠️ Mysql connect failed(Unknown Error):")
        for e_info in traceback.format_exception(*sys.exc_info()):
            for _ in e_info[:-1].split("\n"):
                log.error(_)
    else:
        log.success('mysql is ok')

    try:
        r = redis.StrictRedis(host=glom(db_conf, 'redis.host'),
                              port=glom(db_conf, 'redis.port'),
                              username=glom(db_conf, 'redis.user', default=None),
                              password=glom(db_conf, 'redis.password', default=None),
                              max_connections=glom(db_conf, 'redis.max_conn', default=200),
                              db=glom(db_conf, 'redis.db', default=1),
                              retry_on_timeout=glom(db_conf, 'redis.retry_on_timeout', default=True),
                              socket_timeout=glom(db_conf, 'redis.socket_timeout', default=5)
                              )
        r.ping()

    except ConnectionError:
        log.error(f"⚠️ Redis connect failed:")
        for e_info in traceback.format_exception(*sys.exc_info()):
            for _ in e_info[:-1].split("\n"):
                log.error(_)
    except TimeoutError:
        log.error(f"⚠️ Redis connect failed:")
        for e_info in traceback.format_exception(*sys.exc_info()):
            for _ in e_info[:-1].split("\n"):
                log.error(_)
    except ResponseError:
        log.error(f"⚠️ Redis connect failed:")
        for e_info in traceback.format_exception(*sys.exc_info()):
            for _ in e_info[:-1].split("\n"):
                log.error(_)
    except PathAccessError:
        log.error(f"⚠️ Parse db conf failed:")
        for e_info in traceback.format_exception(*sys.exc_info()):
            for _ in e_info[:-1].split("\n"):
                log.error(_)
    except Exception:
        log.error(f"⚠️ Redis connect failed(Unknown Error):")
        for e_info in traceback.format_exception(*sys.exc_info()):
            for _ in e_info[:-1].split("\n"):
                log.error(_)
    else:
        log.success('redis is ok')

    try:
        rabbitmq = RabbitmqExt(host=glom(db_conf, "rabbitmq.host"),
                               port=glom(db_conf, "rabbitmq.port"),
                               user=glom(db_conf, 'rabbitmq.user'),
                               password=glom(db_conf, "rabbitmq.password"),
                               vhost=glom(db_conf, 'rabbitmq.vhost'))

        rabbitmq.conn.ensure_connection(max_retries=2)

    except kb_exp.OperationalError:
        log.error("⚠️ Rabbitmq connect failed:")
        for e_info in traceback.format_exception(*sys.exc_info()):
            for _ in e_info[:-1].split("\n"):
                log.error(_)

    except AccessRefused:
        log.error("⚠️ Rabbitmq connect failed(Access Refused):")
        for e_info in traceback.format_exception(*sys.exc_info()):
            for _ in e_info[:-1].split("\n"):
                log.error(_)

    except NotAllowed:
        log.error("⚠️ Rabbitmq connect failed(Vhost Not Found):")
        for e_info in traceback.format_exception(*sys.exc_info()):
            for _ in e_info[:-1].split("\n"):
                log.error(_)

    except Exception:
        log.error("⚠️ Rabbitmq connect failed(Unknown Error):")
        for e_info in traceback.format_exception(*sys.exc_info()):
            for _ in e_info[:-1].split("\n"):
                log.error(_)
    else:
        log.success('rabbitmq is ok')


if __name__ == '__main__':
    db_is_ok()
