# coding: utf-8
# @Time : 12/16/21 9:14 AM

from urllib.parse import urlparse

from shino.libs.load import load_obj


class PreExtract:

    def __init__(self, conf):
        self.conf = conf
        self.log = conf['log']

    def handle(self, res_info):
        cls_maps = load_obj(self.conf['pre_extract_module'], suffix='extractor')
        if len(cls_maps) <= 0:
            self.log.warning(f"can not find modifier,please check")
            return res_info

        api = res_info['api']
        netloc = urlparse(api).netloc
        netloc_key = netloc.replace('.', '_')

        if netloc_key not in cls_maps:
            return res_info

        cls_obj = cls_maps[netloc_key]
        instance_obj = cls_obj(self.conf)
        new_res = instance_obj.modify(res_info)

        return new_res
