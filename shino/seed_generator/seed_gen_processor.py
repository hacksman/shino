# coding: utf-8
# @Time : 9/8/21 10:28 AM


from glom import glom
from shino.libs.mysql_ext import MysqlExt
from shino.libs.time_ext import TimeExt
from datetime import datetime
from croniter import croniter
from multiprocessing import Lock
import time
import schedule

from shino.seed_generator.model import SchInfo
from shino.seed_generator.seed_gen_handle import SeedGenHandle

from google.protobuf.json_format import MessageToDict

from shino.libs.rabbitmq_ext import RabbitmqExt
from shino.libs.encrypt import gen_md5

p_lock = Lock()


class SeedGenProcessor:

    def __init__(self, conf):
        self.conf = conf

        self.log = conf['log']

        self.mysql = MysqlExt(**glom(conf, "db.mysql"))

        self.seed_handle = SeedGenHandle(conf)

        self.rabbitmq_conf = glom(conf, "db.rabbitmq")

        self.out_tube = self.rabbitmq_conf['queue_distributor_to_downloader']

        self.rabbitmq = RabbitmqExt(host=self.rabbitmq_conf["host"],
                                    port=self.rabbitmq_conf["port"],
                                    user=self.rabbitmq_conf["user"],
                                    password=self.rabbitmq_conf["password"],
                                    vhost=self.rabbitmq_conf["vhost"])

        self.event = None

    @staticmethod
    def __is_valid(sch_info):
        if all([not sch_info.is_once, not sch_info.appoint_crontab]):
            return False
        return True

    def __cycle_schedule(self, order_dict):
        now_time = datetime.now()
        if not self.event.is_set():
            self.log.info(f"start gen seed")
            for sch_info in self.mysql.select_many("select * from `_seed_sch` where switch='on'"):
                sch_info = SchInfo(**sch_info)
                if not self.__is_valid(sch_info):
                    self.log.warning(f"sch info miss is_once and appoint_crontab：")
                    self.log.warning(f"{sch_info}")
                    continue

                appoint_crontab = sch_info.appoint_crontab
                if appoint_crontab and not croniter.match(appoint_crontab, now_time):
                    # self.log.debug(f"sch_info={sch_info}\t match crontab none")
                    continue

                sch_time = TimeExt.datetime_to_human(t=now_time, fmt="%Y%m%d%H%M")
                sch_info.sch_time = sch_time
                task_key = f"{sch_time}_{sch_info.api}"
                self.log.info(
                    f"find sch work: task_key={task_key}\tappoint_crontab={appoint_crontab}\tis_once={sch_info.is_once}")

                with p_lock:
                    order_dict.update({task_key: sch_info})

                if sch_info.is_once == 1:
                    self.mysql.execute(f"update _seed_sch set switch='off' where _id={sch_info._id}")

    def seed_produce(self, order_dict, event):

        self.event = event

        if self.conf.get('mode') and self.conf.get('mode').lower() == 'debug':
            schedule.every(10).seconds.do(self.__cycle_schedule, order_dict)
        else:
            schedule.every().minutes.do(self.__cycle_schedule, order_dict)

        while not event.is_set():
            schedule.run_pending()
            time.sleep(1)

    def __send_monitor(self, sch_info, count):
        api = sch_info.api
        api_md5 = gen_md5(sch_info.api)
        batch_time = sch_info.sch_time
        batch_no = f"{batch_time}_{api_md5}"
        service = "seed_generator"
        status = "success"
        sql = f"INSERT INTO _service_monitor (count, status, service, batch_no, batch_time, api) VALUES ({count}, '{status}', '{service}', '{batch_no}', '{batch_time}', '{api}') ON DUPLICATE KEY UPDATE count = count + {count};"
        self.mysql.execute(sql)

    def seed_consume(self, order_dict, event):
        while not event.is_set():
            if not order_dict.get_len():
                time.sleep(0.1)
                continue
            with p_lock:
                task_info = order_dict.popitem(False)
            if not task_info:
                time.sleep(0.1)
                continue
            seeds = self.seed_handle.gen_seed(task_info[1])
            seeds_to_dict = [MessageToDict(_, preserving_proto_field_name=True) for _ in seeds]
            self.rabbitmq.send_many(seeds_to_dict, self.out_tube)
            self.__send_monitor(task_info[1], len(seeds_to_dict))
            time.sleep(0.1)
