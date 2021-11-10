# coding: utf-8
# @Time : 9/9/21 9:49 AM

from protos.gen.downloader_pb2 import (CrawlStatus, DownloadRsp, DownloadReq)
from shino.libs.python import to_unicode
from shino.libs.time_ext import TimeExt


class DefaultMiddleware:

    def __init__(self, conf):
        self.conf = conf

    def process_response(self, req, res):
        resp = dict()
        resp["batch_no"] = req["batch_no"]
        resp["api"] = req["api"]
        resp['url'] = req['url']
        resp["download_time"] = TimeExt.datetime_to_human()
        resp["content"] = []
        resp["http_code"] = 0
        resp["elapsed"] = -1
        if res:
            resp["http_code"] = res.status_code
            resp["elapsed"] = res.elapsed.total_seconds()
            resp["content_type"] = res.headers.get("content-type")
            resp["content"] = to_unicode(res.content)
        if hasattr(req, "identify_status"):
            resp["status"] = req.identify_status
        else:
            if resp.get("http_code") == 200:
                resp["status"] = CrawlStatus.CRAWL_SUCCESS
            else:
                resp["status"] = CrawlStatus.CRAWL_FAIL
        resp["req_info"] = DownloadReq(**req)
        return DownloadRsp(**resp)
