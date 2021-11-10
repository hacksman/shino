# coding: utf-8
# @Time : 9/9/21 10:40 AM


import time

from glom import glom
from google.protobuf.json_format import MessageToDict
from queue import Empty

from shino.extractor.extract_handle import ExtractHandle
from shino.libs.rabbitmq_ext import RabbitmqExt
from shino.libs.mysql_ext import MysqlExt


class ExtractProcessor:

    def __init__(self, conf):
        self.conf = conf
        self.log = conf.get("log")
        self.extractor_handle = ExtractHandle(conf)

        self.rabbitmq_conf = glom(self.conf, "db.rabbitmq")
        self.input_tube = self.rabbitmq_conf['queue_downloader_to_extractor']
        self.out_tube_extract_info = self.rabbitmq_conf['queue_extractor_to_cleaner']
        self.out_tube_download_req = self.rabbitmq_conf['queue_distributor_to_downloader']
        self.rabbitmq = RabbitmqExt(host=self.rabbitmq_conf["host"],
                                    port=self.rabbitmq_conf["port"],
                                    user=self.rabbitmq_conf["user"],
                                    password=self.rabbitmq_conf["password"],
                                    vhost=self.rabbitmq_conf["vhost"])

        self.mysql = MysqlExt(**glom(conf, "db.mysql"))

    def __send_monitor(self, res_dict):
        batch_no = res_dict["batch_no"]
        api = res_dict["api"]
        batch_time = batch_no.split("_")[0]
        count = 1
        service = "extract"
        status = "success"
        sql = f"INSERT INTO _service_monitor (count, status, service, batch_no, batch_time, api) VALUES ({count}, '{status}', '{service}', '{batch_no}', '{batch_time}', '{api}') ON DUPLICATE KEY UPDATE count = count + {count};"
        self.mysql.execute(sql)

    def do_job(self, job_event):
        while not job_event.is_set():
            try:
                res_msg = self.rabbitmq.receive(self.input_tube)
                res_msg = self.extractor_handle.pre_extract(res_msg)
                parse_rules = self.extractor_handle.get_parse_rules(res_msg)

                # parse content
                for per_rule in parse_rules:
                    parse_results = self.extractor_handle.extract_content(res_msg, per_rule)
                    pack_results = self.extractor_handle.pack_extract_data(res_msg, per_rule, parse_results)
                    parse_msg_dict = MessageToDict(pack_results, preserving_proto_field_name=True)
                    time.sleep(2)
                    self.rabbitmq.send(parse_msg_dict, self.out_tube_extract_info)

                # gen next page
                for per_rule in parse_rules:
                    page_links = self.extractor_handle.gen_page_req(res_msg, per_rule)
                    for req_msg in page_links:
                        req_msg_dict = MessageToDict(req_msg, preserving_proto_field_name=True)
                        self.rabbitmq.send(req_msg_dict, self.out_tube_download_req)

                # gen sub links
                for per_rule in parse_rules:
                    parse_sub_links = self.extractor_handle.extract_content(res_msg, per_rule, link_type="SUB_URL")
                    sub_links = self.extractor_handle.gen_sub_page_req(res_msg, parse_sub_links)
                    for req_msg in sub_links:
                        req_msg_dict = MessageToDict(req_msg, preserving_proto_field_name=True)
                        self.rabbitmq.send(req_msg_dict, self.out_tube_download_req)

                self.__send_monitor(res_msg)

            except Empty as e:
                self.log.info(f"queue:「{self.input_tube}」 empty....")
                time.sleep(2)
            pass
