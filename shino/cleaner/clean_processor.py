# coding: utf-8
# @Time : 9/9/21 10:53 AM

import time
from queue import Empty

from glom import glom
from google.protobuf.json_format import MessageToDict

from protos.gen.extractor_pb2 import ExtractInfo
from shino.cleaner.clean_handle import CleanHandler
from shino.libs.rabbitmq_ext import RabbitmqExt
from shino.libs.mysql_ext import MysqlExt


class CleanProcessor:

    def __init__(self, conf):
        self.conf = conf
        self.log = conf['log']
        self.cleaner = CleanHandler(conf)

        self.rabbitmq_conf = glom(self.conf, "db.rabbitmq")
        self.input_tube = self.rabbitmq_conf['queue_extractor_to_cleaner']
        self.out_tube = self.rabbitmq_conf['queue_cleaner_to_saver']
        self.rabbitmq = RabbitmqExt(host=self.rabbitmq_conf["host"],
                                    port=self.rabbitmq_conf["port"],
                                    user=self.rabbitmq_conf["user"],
                                    password=self.rabbitmq_conf["password"],
                                    vhost=self.rabbitmq_conf["vhost"])

        self.mysql = MysqlExt(**glom(conf, "db.mysql"))

    def __send_monitor(self, extract_dict):
        batch_no = extract_dict["batch_no"]
        api = extract_dict["api"]
        batch_time = batch_no.split("_")[0]
        count = 1
        service = "cleaner"
        status = "success"
        sql = f"INSERT INTO _service_monitor (count, status, service, batch_no, batch_time, api) VALUES ({count}, '{status}', '{service}', '{batch_no}', '{batch_time}', '{api}') ON DUPLICATE KEY UPDATE count = count + {count};"
        self.mysql.execute(sql)

    def do_job(self, job_event):
        while not job_event.is_set():
            try:
                extract_msg = self.rabbitmq.receive(self.input_tube)
                # self.log.info(f"request_msg\t{clean_msg}")
                clean_rsp = self.cleaner.clean(ExtractInfo(**extract_msg))
                # self.log.debug(f'do_job {len(clean_rsp.content)}')
                final_data_msg_dict = MessageToDict(clean_rsp, preserving_proto_field_name=True)
                self.rabbitmq.send(final_data_msg_dict, self.out_tube)
                self.__send_monitor(extract_msg)
            except Empty:
                self.log.info(f"queue:「{self.input_tube}」 empty....")
                time.sleep(2)
            except BaseException as e:
                self.log.error(f"consume error happened:")
                self.log.exception(e)
            time.sleep(0.01)
        self.log.info(f"s_cleaner job exited.Bye Bye!")
