# coding: utf-8
# @Time : 9/9/21 9:47 AM


import time
from queue import Empty

from glom import glom
from google.protobuf.json_format import MessageToDict

from shino.downloader.download_handle import DownloadHandler
from shino.libs.mysql_ext import MysqlExt
from shino.libs.rabbitmq_ext import RabbitmqExt


class DownloadProcessor:

    def __init__(self, conf):
        self.conf = conf
        self.log = conf.get("log")
        self.downloader = DownloadHandler(conf)

        self.rabbitmq_conf = glom(self.conf, "db.rabbitmq")
        self.input_tube = self.rabbitmq_conf['queue_distributor_to_downloader']
        self.out_tube = self.rabbitmq_conf['queue_downloader_to_extractor']
        self.rabbitmq = RabbitmqExt(host=self.rabbitmq_conf["host"],
                                    port=self.rabbitmq_conf["port"],
                                    user=self.rabbitmq_conf["user"],
                                    password=self.rabbitmq_conf["password"],
                                    vhost=self.rabbitmq_conf["vhost"])
        self.mysql = MysqlExt(**glom(conf, "db.mysql"))

    def __send_monitor(self, req_dict):
        batch_no = req_dict["batch_no"]
        api = req_dict["api"]
        batch_time = batch_no.split("_")[0]
        count = 1
        service = "downloader"
        status = "success"
        sql = f"INSERT INTO _service_monitor (count, status, service, batch_no, batch_time, api) VALUES ({count}, '{status}', '{service}', '{batch_no}', '{batch_time}', '{api}') ON DUPLICATE KEY UPDATE count = count + {count};"
        self.mysql.execute(sql)

    def do_job(self, job_event):
        while not job_event.is_set():
            try:
                req_msg = self.rabbitmq.receive(self.input_tube)
                self.log.info(f"request_msg\t{req_msg}")
                download_rsp = self.downloader.download(req_msg)
                # self.log.debug(f'do_job {len(download_rsp.content)}')
                rsp_msg_dict = MessageToDict(download_rsp, preserving_proto_field_name=True)
                self.rabbitmq.send(rsp_msg_dict, self.out_tube)
                self.__send_monitor(req_msg)
            except Empty:
                self.log.info(f"queue:「{self.input_tube}」 empty....")
                time.sleep(2)
            except BaseException as e:
                self.log.error(f"consume error happened:")
                self.log.exception(e)
            time.sleep(0.01)
        self.log.info(f"s_downloader job exited.Bye Bye!")
