# coding: utf-8
# @Time : 9/9/21 10:53 AM


import json

from glom import glom
from google.protobuf.json_format import MessageToDict

from shino.libs.mysql_ext import MysqlExt
from protos.gen.cleaner_pb2 import CleanInfo


class CleanHandler:
    _MYSQL_TO_PY_MAP = {
        "String": str,
        "INTEGER": int,
        "Text": str,
        "SMALLINT": int,
        "TINYINT": int,
        "FLOAT": float,
        "BOOLEAN": lambda x: x,
        "JSON": lambda x: x,
    }

    def __init__(self, conf):
        self.conf = conf
        self.log = conf["log"]
        self.mysql_conn = MysqlExt(**glom(conf, "db.mysql"))

    def pre_clean(self, extract_info):
        return extract_info

    def nomalize(self, extract_info):
        return extract_info

    def _type_convert(self, results, schema):
        new_results = []
        for per_result in results:
            new_item = {}
            for field, f_value in schema.items():
                if field == "_id":
                    continue
                f_type = f_value["f_type"]
                if_error_set_default = f_value.get("if_error_set_default")
                value_type = self._MYSQL_TO_PY_MAP[f_type]
                try:
                    value = value_type(per_result[field])
                    new_item[field] = value
                except ValueError as e:
                    self.log.debug(f"Clean {field} error happened,need {f_type} type value, but "
                                   f"got {type(per_result[field])} type:{field}={per_result[field]}")
                    self.log.debug(e)
                    new_item[field] = if_error_set_default
                except Exception as e:
                    self.log.error(f"Exception:")
                    self.log.exception(e)
                    new_item[field] = if_error_set_default
                    self.log.debug(f"per_result={per_result}")
            new_results.append(new_item)
        return new_results

    def type_covert(self, extract_info):
        topic_id = extract_info["topic_id"]
        topic_info = self.mysql_conn.select_one(f'select * from `_topic` where _id={topic_id}')
        schema = json.loads(topic_info["schema"])
        all_results = extract_info["extract_data"]
        converted_data = self._type_convert(all_results, schema)
        extract_info["extract_data"] = converted_data
        return extract_info

    def pack_clean_info(self, extract_info):
        clean_info = {
            "batch_no": extract_info["batch_no"],
            "api": extract_info["api"],
            "cl_status": '1',
            "topic_id": extract_info["topic_id"],
            "clean_data": json.dumps(extract_info["extract_data"]),
        }
        clean_info_msg = CleanInfo(**clean_info)
        return clean_info_msg

    def clean(self, extract_info_msg):
        extract_info_dict = MessageToDict(extract_info_msg, preserving_proto_field_name=True)
        extract_info_dict["extract_data"] = json.loads(extract_info_dict["extract_data"])
        for per_method in [self.pre_clean, self.nomalize, self.type_covert]:
            extract_info_dict = per_method(extract_info_dict)
        clean_info_msg = self.pack_clean_info(extract_info_dict)
        return clean_info_msg
