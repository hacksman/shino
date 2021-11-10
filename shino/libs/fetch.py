# coding: utf-8
# @Time : 7/8/21 12:14 PM

import random

import urllib3
import requests
from retrying import retry

from shino.libs.log_ext import LogExt

from conf import PropertiesCenter

logger = LogExt('fetch.log').get_logger

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class FakeChromeUA:
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_12_6)'
    ]

    chrome_version = f'Chrome/{random.randint(55, 62)}.0.{random.randint(0, 3200)}.{random.randint(0, 140)}'

    @classmethod
    def get_ua(cls):
        return ' '.join(['Mozilla/5.0', random.choice(cls.os_type), 'AppleWebKit/537.36',
                         '(KHTML, like Gecko)', cls.chrome_version, 'Safari/537.36']
                        )


def get_proxy():
    proxies = {"http": PropertiesCenter.get('libs.fetch.proxy_http_url'),
               "https": PropertiesCenter.get('libs.fetch.proxy_http_url')}
    return proxies


def need_retry(exception):
    result = isinstance(exception, (requests.ConnectionError, requests.exceptions.ReadTimeout))
    if result:
        logger.warning(f"Exception[{type(exception)}]\toccurred retrying...")
    return result


def fetch(url: str, use_proxy: bool = False, **kwargs):
    @retry(stop_max_attempt_number=PropertiesCenter.get('libs.fetch.max_retry_req_times'),
           wait_random_min=PropertiesCenter.get('libs.fetch.retry_random_min_wait'),
           wait_random_max=PropertiesCenter.get('libs.fetch.retry_random_max_wait'),
           retry_on_exception=need_retry)
    def _fetch(url: str, **kwargs):
        kwargs.update({"verify": False})
        kwargs.update({"timeout": kwargs.get("timeout") or PropertiesCenter.get('libs.fetch.default_req_timeout')})
        if use_proxy:
            proxy = get_proxy()
            if not proxy:
                raise requests.ConnectionError(f"request get proxy failed")
            kwargs.update({"proxies": proxy})

        headers = kwargs.get("headers", {})

        headers["user-agent"] = headers.pop("user-agent", FakeChromeUA.get_ua())
        headers["Accept-Encoding"] = headers.pop("Accept-Encoding", 'gzip, deflate, sdch')
        headers["Accept-Language"] = headers.pop("Accept-Language", 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3')
        headers["Accept"] = headers.pop("Accept", 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        headers["Connection"] = headers.pop("Connection", 'keep-alive')

        kwargs["headers"] = headers
        if kwargs.get("method") in ["post", "POST"]:
            kwargs.pop("method", None)
            response = requests.post(url, **kwargs)
        else:
            response = requests.get(url, **kwargs)
        if response.status_code != 200:
            raise requests.ConnectionError(f"request status code should be 200! but got {response.status_code}")
        return response

    try:
        result = _fetch(url, **kwargs)
        return result
    except (requests.ConnectionError, requests.exceptions.ReadTimeout):
        return None
