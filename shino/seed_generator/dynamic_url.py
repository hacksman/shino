# coding: utf-8
# @Time : 9/8/21 9:46 AM
from urllib.parse import urlparse

from shino.libs.load import load_obj


class DynamicUrl:

    def __init__(self, conf):
        self.conf = conf
        self.log = conf['log']

    def change_url(self, sch_info, urls):
        cls_maps = load_obj(self.conf['dynamic_url_module'], suffix='modifier')
        if len(cls_maps) <= 0:
            self.log.warning(f"can not find modifier,please check")
            return urls

        api = sch_info.api
        netloc = urlparse(api).netloc
        netloc_key = netloc.replace('.', '_')

        if netloc_key not in cls_maps:
            return urls

        cls_obj = cls_maps[netloc_key]

        instance_obj = cls_obj(self.conf)

        new_urls = instance_obj.modify(urls)

        return new_urls
