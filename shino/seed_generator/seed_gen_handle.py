# coding: utf-8
# @Time : 9/8/21 9:37 AM

import redis
import pickle

from shino.seed_generator.url_generator import UrlGenerator
from protos.gen.downloader_pb2 import DownloadReq
from glom import glom

from shino.libs.encrypt import gen_md5

from furl import Query

from multiprocessing import Lock

p_lock = Lock()


class SeedGenHandle:

    def __init__(self, conf):
        self.log = conf['log']
        self.conf = conf
        self.url_generator = UrlGenerator(conf)

        redis_conf = glom(self.conf, "db.redis")
        self.redis_conn = redis.StrictRedis(host=redis_conf["host"],
                                            port=redis_conf["port"],
                                            max_connections=redis_conf["max_conn"],
                                            db=redis_conf["seed_withdraw"],
                                            retry_on_timeout=True)

    def _pack_seed(self, sch_info):
        sch_time = sch_info.sch_time
        if not sch_time:
            self.log.warning(f"miss sch time...")
            return
        api_md5 = gen_md5(sch_info.api)
        batch_no = f"{sch_time}_{api_md5}"
        req_url = sch_info.req_url
        url_unpack = req_url.split("|")
        method = "post" if len(url_unpack) == 2 else "get"
        post_data = {} if method == "get" else dict(Query(url_unpack[1].split(":")[1]).params)
        req = DownloadReq(**{
            "batch_no": batch_no,
            "api": sch_info.api,
            "url": url_unpack[0],
            "method": method,
            "post_data": post_data
        })
        return req

    def gen_seed(self, sch_info):
        urls = self.url_generator.gen_url(sch_info)
        total_seeds = []
        for per_url in urls:
            sch_info.req_url = per_url
            # self.log.debug(f"seed={sch_info}")
            seed = self._pack_seed(sch_info)
            if not seed:
                self.log.warning(f"pack seed failed")
            total_seeds.append(seed)
        return total_seeds

    def withdraw_seed(self, order_dict):
        self.log.info(f"start withdraw seed.")
        seed_cnt = order_dict.get_len()
        with p_lock:
            if seed_cnt == 0:
                self.log.success(f"no seed left!")
                return
            pickle_dict = pickle.dumps(order_dict.get_dict())
            self.redis_conn.set("seeds", pickle_dict)
        self.log.success(f"{seed_cnt} seed withdraw")
