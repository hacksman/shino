# coding: utf-8
# @Time : 9/9/21 10:59 AM


import json
import sys
import traceback

import stringcase

from glom import glom
from sqlalchemy import (create_engine, MetaData, inspect)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Table, Column, INTEGER, String, text, TIMESTAMP, JSON, func, BOOLEAN, Text, Index)
from sqlalchemy.dialects.mysql import (TINYINT, SMALLINT, FLOAT)

from google.protobuf.json_format import MessageToDict
from protos.gen.cleaner_pb2 import CleanInfo
from protos.gen.saver_pb2 import SaveStatus
from shino.libs.mysql_ext import MysqlExt
from shino.libs.sqlalchemy_ext import SqlalchemyExt


class SaveHandler:

    def __init__(self, conf):
        self.conf = conf
        self.log = conf['log']

        self.mysql_conf = glom(conf, 'db.mysql')

        self.mysql = MysqlExt(**self.mysql_conf)

        self.engine = self._init_engine()

        self.base = declarative_base()

        self.session = sessionmaker(bind=self.engine)()

    def _init_engine(self):
        conn = f"mysql+pymysql://{self.mysql_conf['user']}:{self.mysql_conf['password']}@{self.mysql_conf['host']}:{self.mysql_conf['port']}/{self.mysql_conf['db']}?charset=utf8mb4"
        engine = create_engine(conn, encoding="utf-8", pool_recycle=1600, pool_pre_ping=True)
        return engine

    def get_topic_by_id(self, topic_id):
        topic_info = self.mysql.select_one(f"select * from _topic where _id={topic_id}")
        return topic_info

    def _dynamic_gen_table(self, topic_info):
        table_name = topic_info["table"]

        if inspect(self.engine).has_table(table_name):
            return True

        schema = json.loads(topic_info['schema'])

        column_infos = {}

        for field, field_attr in schema.items():
            per_column = Column(
                eval(field_attr["f_type"])(int(field_attr["f_max_range"])) if "f_max_range" in field_attr else eval(
                    field_attr["f_type"]),
                nullable=field_attr.get("nullable", True),
                primary_key=field_attr.get("primary_key", False),
                autoincrement=field_attr.get("auto_increment", False),
                comment=field_attr.get("f_comment")
            )
            column_infos[field] = per_column

        c_time_column = Column(TIMESTAMP, server_default=func.now())
        u_time_column = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
        column_base = {"_create_time": c_time_column,
                       "_update_time": u_time_column,
                       "_is_delete": Column(TINYINT, server_default="0"),
                       "__table_args__": (Index("_create_time_desc", c_time_column.desc()),
                                          Index("_update_time_desc", u_time_column.desc()))
                       }

        attr_dict = {
            "__tablename__": table_name,
            **column_infos,
            **column_base,
        }

        class_name = stringcase.pascalcase(table_name)
        type(class_name, (self.base,), attr_dict)

        self.base.metadata.create_all(self.engine)
        return True

    def __send_monitor(self, clean_info_dict):
        batch_no = clean_info_dict["batch_no"]
        api = clean_info_dict["api"]
        batch_time = batch_no.split("_")[0]
        count = len(clean_info_dict["clean_data"])
        service = "saver"
        status = "success"
        sql = f"INSERT INTO _service_monitor (count, status, service, batch_no, batch_time, api) VALUES ({count}, '{status}', '{service}', '{batch_no}', '{batch_time}', '{api}') ON DUPLICATE KEY UPDATE count = count + {count};"
        self.mysql.execute(sql)

    def save(self, clean_info_msg):
        clean_info_dict = MessageToDict(clean_info_msg, preserving_proto_field_name=True)
        clean_info_dict["clean_data"] = json.loads(clean_info_dict["clean_data"])
        topic_id = clean_info_dict["topic_id"]
        topic_info = self.get_topic_by_id(topic_id)
        try:
            self._dynamic_gen_table(topic_info)
        except Exception as e:
            self.log.error("dynamic create table error happened:")
            for e_info in traceback.format_exception(*sys.exc_info()):
                for _ in e_info[:-1].split("\n"):
                    self.log.error(_)
            return SaveStatus(**{'batch_no': clean_info_dict["batch_no"],
                                 'api': clean_info_dict["api"],
                                 'save_status': "-1",
                                 'save_error_code': '4401'
                                 })
        table_name = topic_info["table"]
        for clean_data in clean_info_dict["clean_data"]:
            data_model = SqlalchemyExt.get_model_by_table(self.base, self.engine, table_name)
            data_obj = SqlalchemyExt.dict_to_obj(clean_data, data_model)
            try:
                self.session.add(data_obj)
                self.session.commit()
            finally:
                self.session.close()

        self.__send_monitor(clean_info_dict)

        return SaveStatus(**{'batch_no': clean_info_dict["batch_no"],
                             'api': clean_info_dict["api"],
                             'save_status': "1"})
