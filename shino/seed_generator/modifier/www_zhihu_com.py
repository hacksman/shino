# coding: utf-8
# @Time : 9/18/21 10:54 AM

from shino.seed_generator.modifier.base import BaseModifier


class Www_Zhihu_ComModifier(BaseModifier):

    def __init__(self, conf):
        self.conf = conf

    def modify(self, urls):
        new_urls = []
        for per_url in urls:
            print(f"u can change url here...", per_url)
            new_urls.append(per_url)
        return new_urls
