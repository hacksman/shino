# coding: utf-8
# @Time : 9/9/21 11:00 AM


import time
from queue import Empty

from glom import glom
from google.protobuf.json_format import MessageToDict

from protos.gen.cleaner_pb2 import CleanInfo
from shino.saver.save_handle import SaveHandler
from shino.libs.rabbitmq_ext import RabbitmqExt


class SaveProcessor:

    def __init__(self, conf):
        self.conf = conf
        self.log = conf['log']

        self.saver = SaveHandler(conf)

        self.rabbitmq_conf = glom(self.conf, "db.rabbitmq")
        self.input_tube = self.rabbitmq_conf['queue_cleaner_to_saver']
        self.rabbitmq = RabbitmqExt(host=self.rabbitmq_conf["host"],
                                    port=self.rabbitmq_conf["port"],
                                    user=self.rabbitmq_conf["user"],
                                    password=self.rabbitmq_conf["password"],
                                    vhost=self.rabbitmq_conf["vhost"])

    def do_job(self, job_event):
        while not job_event.is_set():
            try:
                clean_info_msg = self.rabbitmq.receive(self.input_tube)
                # self.log.info(f"request_msg\t{clean_msg}")
                save_status_rsp = self.saver.save(CleanInfo(**clean_info_msg))
                # self.log.debug(f'do_job {len(clean_rsp.content)}')
                save_status_info = MessageToDict(save_status_rsp, preserving_proto_field_name=True)
            except Empty:
                self.log.info(f"queue:「{self.input_tube}」 empty....")
                time.sleep(2)
            except BaseException as e:
                self.log.error(f"consume error happened:")
                self.log.exception(e)
            time.sleep(0.01)
        self.log.info(f"s_saver job exited.Bye Bye!")
