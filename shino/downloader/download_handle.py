# coding: utf-8
# @Time : 9/9/21 9:39 AM
import random
import time
import traceback

from glom import glom
from copy import deepcopy
from shino.downloader.downloader.downloader import Downloader
from shino.downloader.middleware_manager import MiddlewareManager
from protos.gen.downloader_pb2 import (CrawlStatus, DownloadRsp, DownloadReq)


class DownloadHandler:

    def __init__(self, conf):
        self.log = conf.get("log")
        self.conf = conf
        self.middleware_manager = MiddlewareManager(conf)
        self.downloader = Downloader(conf)

    def download(self, req):
        self.log.info(
            f"start_crawl\turl:{req.get('url')}\tmethod:{req.get('method')}\tdownload_type:{req.get('download_type')}")
        start = time.time()
        res = DownloadRsp(batch_no=req["batch_no"], api=req["api"], status=CrawlStatus.CRAWL_FAIL,
                          req_info=DownloadReq(**req))
        try:
            req_times = req.get('retry_times') or glom(self.conf, "default_request_params.retry_times")
            for _ in range(req_times):
                req = deepcopy(req)
                self.middleware_manager.process_request(req)
                res = self.downloader.download(req)
                if not res:
                    continue
                self.log.info(f"result_code ==: {res.status_code}")
                res = self.middleware_manager.process_response(req, res)
                if res.status == CrawlStatus.CRAWL_SUCCESS:
                    break
                time.sleep(random.randint(*glom(self.conf, "default_request_params.next_retry_sleep")))
        except Exception as e:
            self.log.error(f"url:{req.get('url')}\terror_msg:{str(traceback.format_exc())}")
        finally:
            content_len = -1
            if res.content:
                content_len = len(res.content)
            self.log.info(f"finish_crawl\tuse_time:{str(time.time() - start)}\t"
                          f"lens:{content_len}\tstatus:{res.status}\turl:{req.get('url')}")
        return res
