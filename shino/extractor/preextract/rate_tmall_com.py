# coding: utf-8
# @Time : 12/16/21 9:22 AM

import json

from shino.extractor.preextract.base import BaseExtractor


class Rate_Tmall_ComExtractor(BaseExtractor):

    def __init__(self, conf):
        self.conf = conf
        self.log = conf['log']

    def modify(self, res_infos):
        return res_infos
