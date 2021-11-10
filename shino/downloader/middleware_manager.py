# coding: utf-8
# @Time : 9/9/21 9:47 AM

from shino.libs.load import load_obj


class MiddlewareManager:

    def __init__(self, conf):
        self.conf = conf
        self.log = conf.get("log")
        mw_cls_dict = load_obj(conf.get("middleware_module"), suffix="middleware")
        self.middlewares = {
            'request': [],
            'response': []
        }
        for mw_name in self.conf.get("middlewares"):
            mw_cls = mw_cls_dict[mw_name]
            mw_instance = mw_cls(conf)
            if hasattr(mw_cls, "process_request"):
                self.middlewares["request"].append(mw_instance)
            if hasattr(mw_cls, "process_response"):
                self.middlewares["response"] += [mw_instance]

    def process_request(self, req):
        for mw in self.middlewares["request"]:
            mw.process_request(req)

    def process_response(self, req, res):
        for mw in self.middlewares["response"]:
            res = mw.process_response(req, res)
        return res
