# coding: utf-8
# @Time : 9/9/21 9:49 AM


import json
import requests
import requests.packages.urllib3
from requests.exceptions import (ConnectTimeout, HTTPError, ProxyError, ConnectionError)
requests.packages.urllib3.disable_warnings()

from glom import glom


class SimpleDownloader:
    download_kwargs = {
        "allow_redirects": True,
        "params": None,
        "data": None,
        "headers": None,
        "cookies": None,
        "files": None,
        "auth": None,
        "timeout": None,
        "proxies": None,
        "stream": None,
        "verify": None,
        "cert": None,
        "json": None,
    }

    def __init__(self, conf):
        self.conf = conf
        self.log = conf.get('log')

    def _req_to_kw(self, req):
        kw = {}
        for k, v in self.download_kwargs.items():
            if hasattr(req, k) and getattr(req, k) is not None:
                kw[k] = getattr(req, k)
            else:
                kw[k] = v
        kw['data'] = req.get('post_data')
        try:
            if isinstance(req.get('post_data'), dict):
                if req.get('post_data') and "payload" in req.get("post_data"):
                    req['post_data'].pop("payload")
                    kw['data'] = json.dumps(req.post_data)
        except Exception as e:
            self.log.error(f"payload 请求参数 dump 出错：「{req}」")
            self.log.exception(e)
        kw["headers"] = req.get('http_header')
        kw['timeout'] = req.get('time_out') or glom(self.conf, "default_request_params.time_out")
        return kw

    def download(self, req):
        url = req['url']
        method = req.get('method') or 'get'
        req_kw = self._req_to_kw(req)
        res = None
        try:
            if method == "get":
                if "data" in req_kw:
                    req_kw.pop('data')
                # print(f"最终的请求形式：「{req_kw}」")
                res = requests.get(url, **req_kw)
            elif method == "post":
                res = requests.post(url, **req_kw)
            else:
                self.log.error(f"method error: {req_kw.get('method')}")
                return
        except ProxyError as e:
            req.identify_status = 8
            self.log.error(f"{self.__class__.__name__}\turl:{url}\tproxy:{req_kw['proxies']}\tping\tfail")
            self.log.info(f"{str(res)}")
        except HTTPError or ConnectTimeout or ConnectionError as e:
            req.identify_status = 7
            self.log.error(f"{self.__class__.__name__}\turl:{url}\tmethod:{method}\tproxy\tfail")
            self.log.info(f"{str(res)}")
        except Exception as e:
            self.log.error(f"{self.__class__.__name__}\turl:{url}\tmethod:{method}\texcept:{e}")
            self.log.info(f"{str(res)}")
        return res

    def stop(self):
        pass
