# coding: utf-8
# @Time : 9/9/21 9:50 AM


import random


class UserAgentMiddleware:

    def __init__(self, conf):
        self.conf = conf

    @staticmethod
    def __get_fake_ua():
        os_type = [
            '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
            '(Macintosh; Intel Mac OS X 10_12_6)'
        ]

        chrome_version = f'Chrome/{random.randint(55, 62)}.0.{random.randint(0, 3200)}.{random.randint(0, 140)}'

        return ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                         '(KHTML, like Gecko)', chrome_version, 'Safari/537.36'])

    def process_request(self, req):
        user_agent = self.__get_fake_ua()
        http_header = req.get("http_header")
        if isinstance(http_header, dict):
            if not http_header.get("User-Agent"):
                req['http_header']["user-agent"] = user_agent
        else:
            if not http_header:
                http_header = {"user-agent": user_agent}
        http_header["Connection"] = 'close'
        req["http_header"] = http_header
