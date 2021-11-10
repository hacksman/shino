# coding: utf-8
# @Time : 9/9/21 9:50 AM


import json

from furl import furl
from glom import glom

from shino.libs.mysql_ext import MysqlExt


class HeadersMiddleware:

    def __init__(self, conf):
        self.conf = conf
        self.mysql_conf = glom(conf, "db.mysql")
        self.mysql_conn = MysqlExt(**self.mysql_conf)

    def process_request(self, req):
        req_url = req.get('url')
        host = furl(req_url).host
        request_depend = self.mysql_conn.select_one(f'select * from _request_depend where host="{host}"')
        # todo: support to many header
        if request_depend:
            headers_ext = json.loads(request_depend.get("headers_ext"))[0] or {}

            http_header = req.get("http_header") or {}

            http_header.update(headers_ext)
            req["http_header"] = http_header
